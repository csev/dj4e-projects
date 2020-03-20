from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings

class Project(models.Model) :
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    url = models.URLField(max_length=200,
            help_text='Please provide the url of the working project')
    source = models.URLField(max_length=200, null=True, blank=True,
            help_text='Please provide the url to the source of the project (i.e on GitHub)')
    text = models.TextField(verbose_name='A description of the project')
    note = models.TextField(null=True, blank=True,
            verbose_name='A private note to the site administrator (i.e. not the public)')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owners_project")

    published = models.BooleanField(null=True, blank=True)

    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='comments_projects')

    # Favorites
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Fav', related_name='favorite_projects')

    # Picture
    picture = models.BinaryField(null=True, blank=True, editable=True,
            verbose_name='Screen shot of the application')
    content_type = models.CharField(max_length=256, null=True, blank=True, help_text='The MIMEType of the file')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        return self.title

class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(4, "Comment must be greater than 3 characters")]
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_comments')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
            related_name="project_comment_owners")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'

class Fav(models.Model) :
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
            related_name='fav_project_owners')

    # https://docs.djangoproject.com/en/2.1/ref/models/options/#unique-together
    class Meta:
        unique_together = ('project', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.project.title[:10])

