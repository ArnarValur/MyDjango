from django.db import models


# The Page Model:
class Page(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='children')
    published = models.BooleanField(default=False)
    order = models.PositiveIntegerField(unique=True, default=0)

    # TODO metadata integration: metadata should be optional for each page. Here are only 3 simple fields.
    # SEO optimization idea: django-meta package.
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title
