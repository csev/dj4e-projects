from django.urls import path, reverse_lazy
from . import views

app_name='projects'
urlpatterns = [
    path('', views.ProjectListView.as_view(), name='all'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='detail'),
    path('project/create', 
        views.ProjectCreateView.as_view(success_url=reverse_lazy('projects:all')), name='create'),
    path('project/<int:pk>/update', 
        views.ProjectUpdateView.as_view(success_url=reverse_lazy('projects:all')), name='update'),
    path('project/<int:pk>/delete', 
        views.ProjectDeleteView.as_view(success_url=reverse_lazy('projects:all')), name='delete'),
]

# We use reverse_lazy in urls.py to delay looking up the view until all the paths are defined
