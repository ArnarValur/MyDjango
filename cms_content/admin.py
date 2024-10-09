from urllib.parse import urlparse

from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import format_html

from .models import Page, Post, Link


# Register your models here.
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'page_status', 'page_link_location', 'order', 'show_in_position')
    list_filter = ('page_status',)
    list_editable = ('page_link_location', 'page_status', 'order', 'show_in_position')
    search_fields = ('title', 'content')
    #TODO add absolute URL to the prepopulated_fields
    prepopulated_fields = {
        'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'parent', 'slug', 'content', 'page_status')
        }),
        ('Navigation', {
            'classes': ['collapse'],
            'fields': ('page_link_location', 'order', 'show_in_position')
        }),
        ('Metadata', {
            'classes': ['collapse'],
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        })
    )

    #TODO:Implement the following method to create a full url link_model for page and add to prepopulated_fields
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    get_absolute_url.short_description = 'URL'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status', 'created', 'updated')
    list_filter = ('status', 'created', 'updated', 'author')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'excerpt', 'author', 'status', 'views')
        }),
        ('Metadata', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        })
    )


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    # Change the list view with custom template
    # change_list_template = 'cms_content/link_model/change_list.html'
    list_display = (
        'label', 'slug', 'page_admin_link', 'status', 'location', 'order', 'external_url', 'view_page_link')
    list_filter = ('status',)
    search_fields = ('label', 'url', 'page__title',)
    prepopulated_fields = {'slug': ('label',)}
    fieldsets = (
        (None, {
            'fields': ('label', 'page', 'slug', 'status', 'order')
        }),
        ('External URL', {
            'classes': ['collapse'],
            'fields': ('url',)
        }),
    )

    def page_admin_link(self, obj):
        if obj.page:
            page_link = reverse('admin:cms_content_page_change', args=[obj.page.id])
            return format_html('<a href="{}">{}</a>', page_link, obj.page.title)
        return ' '

    page_admin_link.short_description = 'Edit Page'

    #TODO: Add eye icon on the view page link_model
    def view_page_link(self, obj):
        if obj.page:
            front_end_link = f"/{obj.page.slug}/"  #TODO: Adjust the front end link_model to match the actual front end URL
            return format_html('<a href="{}" target="_blank">ViewIcon</a>', front_end_link, obj.page.title)
        return ' '

    view_page_link.short_description = 'View Page'

    def external_url(self, obj):
        if obj.url:
            url = obj.url
            return format_html('<a href="https://{}" target="_blank">{}</a>', url, obj.label)
        return ' '

    external_url.short_description = 'External URL'


