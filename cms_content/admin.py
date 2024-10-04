from django.contrib import admin
from django.db import models
from .models import Page


# Register your models here.
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published', 'order')
    list_filter = ('published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'parent', 'published', 'order')
        }),
        ('Metadata', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        })
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Only set initial data for new objects
            max_order = Page.objects.aggregate(models.Max('order'))['order__max']
            form.base_fields['order'].initial = max_order + 1 if max_order is not None else 1
        return form

