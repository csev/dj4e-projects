from django.contrib import admin

# Register your models here.

from projects.models import Project, Comment, Fav

# Define the admin class
class ProjectAdmin(admin.ModelAdmin):
    exclude = ('picture', 'content_type')

# Register the admin class with the associated model
admin.site.register(Project, ProjectAdmin)

admin.site.register(Comment)
admin.site.register(Fav)
