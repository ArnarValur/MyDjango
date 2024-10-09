import uuid
from typing import Optional

from django.db import models
from django.db.models import Manager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

# Helper functions for the models:

# Status choices:
STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('private', 'Private'),
]

# Link position choices:
LINK_LOCATION_CHOICES = [
    ('navbar', 'Navbar'),
    ('header', 'Header'),
    ('footer', 'Footer'),
    ('sidebar', 'Sidebar'),
    ('unsorted', 'Unsorted'),
]


# The Page Model:
class Page(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True)
    parent: Optional['Page'] = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='children')
    page_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    page_link_location = models.CharField(max_length=10, choices=LINK_LOCATION_CHOICES, default='unsorted')
    show_in_position = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    # TODO metadata integration: metadata should be optional for each page. Here are only 3 simple fields.
    # SEO optimization idea: django-meta package.
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.parent:
            self.slug = f"{self.parent.slug}/{slugify(self.title)}"
        else:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        if not getattr(self, '_skip_link_update', False):
            # Update or create the associated Link object
            link, created = Link.objects.get_or_create(page=self)
            link.label = self.title
            link.slug = self.slug  # Use the page's slug for the link as well
            link.location = self.page_link_location
            link.status = self.page_status
            link.order = self.order
            link.save()


class Link(models.Model):
    label = models.CharField(max_length=200, blank=False, null=False)
    slug = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    page = models.OneToOneField(Page, on_delete=models.CASCADE, related_name='link', blank=True, null=True)
    location = models.CharField(max_length=10, choices=LINK_LOCATION_CHOICES, default='unsorted')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    order = models.PositiveIntegerField(default=0)

    objects: Manager

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.label:  # Only set the label if it's not already set
            self.label = self.page.title if self.page else ''
        if not self.slug:  # Only generate the slug if it's not already set
            self.slug = slugify(self.label)
            while Link.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.label)}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)


# The Post Model:
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


@receiver(post_save, sender=Link)
def update_page_from_link(sender, instance, **kwargs):
    if instance.page:
        instance.page.title = instance.label
        instance.page.slug = instance.slug
        if not instance.page.page_link_location:
            instance.page.page_link_location = instance.location
        if not instance.page.page_status:
            instance.page.page_status = instance.status
        instance.page.order = instance.order
        instance.page._skip_link_update = True
        instance.page.save()
