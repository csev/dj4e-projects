from django.urls import path, reverse_lazy
from . import views
from . import models
from projects.models import Project, Comment, Fav
from libs.owner import OwnerDeleteView
from django.views.generic import TemplateView

app_name='projects'
urlpatterns = [
    path('', views.MyListView.as_view(model=Project, template_name=app_name+"/list.html"), name='all'),
    path('project/<int:pk>', views.MyDetailView.as_view(model=Project, template_name=app_name+"/detail.html"), name='detail'),
    path('project/create',
        views.MyCreateView.as_view(model=Project, template=app_name+'/form.html',success_url=reverse_lazy(app_name+':all')), name='create'),
    path('project/<int:pk>/update',
        views.MyUpdateView.as_view(model=Project, template=app_name+'/form.html', success_url=reverse_lazy(app_name+':all')), name='update'),
    path('project/<int:pk>/delete',
        OwnerDeleteView.as_view(model=Project,template_name=app_name+"/delete.html",success_url=reverse_lazy(app_name+':all')), name='delete'),
    path('project/<int:pk>/comment',
        views.CommentCreateView.as_view(app_name=app_name), name='comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(
            model=Comment,
            app_name=app_name,
            template_name=app_name+"/comment_delete.html",
            success_url=reverse_lazy(app_name+':all')),
        name='comment_delete'),
    path('project_picture/<int:pk>', views.stream_file, name='picture'),
    path('project/<int:pk>/favorite',
        views.AddFavoriteView.as_view(), name='favorite'),
    path('project/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='unfavorite'),
]

