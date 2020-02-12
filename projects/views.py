from projects.models import Project

from django.views import View
from django.views import generic
from django.shortcuts import render

from projects.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class ProjectListView(OwnerListView):
    model = Project
    template_name = "projects/list.html"

class ProjectDetailView(OwnerDetailView):
    model = Project
    template_name = "projects/detail.html"

class ProjectCreateView(OwnerCreateView):
    model = Project
    fields = ['title', 'text']
    template_name = "projects/form.html"

class ProjectUpdateView(OwnerUpdateView):
    model = Project
    fields = ['title', 'text']
    template_name = "projects/form.html"

class ProjectDeleteView(OwnerDeleteView):
    model = Project
    template_name = "projects/delete.html"

