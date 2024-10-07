import uuid
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

# Helper functions for the models:
const = STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('private', 'Private'),
    ]


# The Page Model:
class Page(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='children')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    #order = models.PositiveIntegerField(unique=True, default=0)

    # TODO metadata integration: metadata should be optional for each page. Here are only 3 simple fields.
    # SEO optimization idea: django-meta package.
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title


#The Post Model:
class Post(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, blank=False, null=False, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    content = models.TextField(blank=True)
    excerpt = models.TextField(blank=True)

    #TODO implement author field with default value as the logged in user (that creates the post)
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    #TODO install Pillow package for image processing
    #feature_image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    #TODO Think about tags implementation
    #tags = models.ManyToManyField('Tag', blank=True)
    #TODO Implement views counter (global in this model and reuse it in other models)
    views = models.PositiveIntegerField(default=0)

    # TODO metadata integration: metadata should be optional for each post. Here are only 3 simple fields.
    # TODO SEO optimization idea: django-meta package.
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    #Function to get the string representation of the post by its title
    def __str__(self):
        return self.title

    #Function to get the absolute URL of the post by its slug
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.slug)])

    #Function to save the post with a slug if it does not have one
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{str(uuid.uuid4().hex[:8])}"
        super().save(*args, **kwargs)