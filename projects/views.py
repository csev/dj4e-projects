from projects.models import Project, Comment, Fav
from projects.forms import CommentForm, CreateForm

from django.views import View
from django.views import generic
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime
from libs.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

from libs.misc import cleanup

class MyListView(OwnerListView):
    model = Project
    def get_queryset(self):
        cleanup(self.model)
        return super(MyListView, self).get_queryset()

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Project.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            query = Q(title__contains=strval)
            query.add(Q(text__contains=strval), Q.OR)
            project_list = Project.objects.filter(Q(owner=request.user.id) | Q(published=True)).filter(query).select_related().order_by('-updated_at')[:10]
        else :
            # try both versions with > 4 posts and watch the queries that happen
            project_list = Project.objects.filter(Q(owner=request.user.id) | Q(published=True)).order_by('-updated_at')[:10]
            # objects = Project.objects.select_related().all().order_by('-updated_at')[:10]

        unpublished = Project.objects.filter(published=None).count()
        # print(project_list)
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}]  (A list of rows)
            rows = request.user.favorite_projects.values('id')
            favorites = [ row['id'] for row in rows ]

        # Augment the project_list
        for project in project_list:
            project.natural_updated = naturaltime(project.updated_at)

        ctx = {'project_list' : project_list, 'favorites': favorites, 'search': strval, 'unpublished': unpublished}
        return render(request, self.template_name, ctx)

class MyDetailView(OwnerDetailView):
    model = Project
    def get(self, request, pk) :
        project = Project.objects.get(id=pk)
        comments = Comment.objects.filter(project=project).order_by('-updated_at')[:20]
        comment_form = CommentForm()
        context = { 'project' : project, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

# We can't extend OwnerCreateView because we have a special form and process for files
class MyCreateView(LoginRequiredMixin, View):
    model = Project
    success_url = None   # See urls.py
    template = None   # See urls.py
    def get(self, request) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Adjust the model owner before saving
        inst = form.save(commit=False)
        inst.owner = self.request.user
        inst.save()
        return redirect(self.success_url)

class MyUpdateView(LoginRequiredMixin, View):
    model = Project
    template = None   # See urls.py
    success_url = None   # See urls.py
    def get(self, request, pk) :
        inst = get_object_or_404(Project, id=pk, owner=self.request.user)
        form = CreateForm(instance=inst)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        inst = get_object_or_404(Project, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=inst)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Adjust the model owner before saving
        inst = form.save(commit=False)
        inst.owner = self.request.user
        inst.save()
        return redirect(self.success_url)

class CommentCreateView(View):
    app_name = None # specify in urls.py
    def post(self, request, pk) :
        a = get_object_or_404(Project, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, project=a)
        comment.save()
        return redirect(reverse_lazy(self.app_name+':detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    app_name = None # override from urls.py

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        project = self.object.project
        return reverse_lazy(self.app_name+':detail', args=[project.id])

def stream_file(request, pk) :
    project = get_object_or_404(Project, id=pk)
    response = HttpResponse()
    response['Content-Type'] = project.content_type
    response['Content-Length'] = len(project.picture)
    response.write(project.picture)
    return response

# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Project, id=pk)
        fav = Fav(user=request.user, project=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Project, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, project=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()

