from django.contrib import admin

# Register your models here.

from projects.models import Project, Comment, Fav

admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Fav)
