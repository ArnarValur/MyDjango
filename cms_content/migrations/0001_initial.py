# Generated by Django 5.1.1 on 2024-10-09 15:44

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('content', models.TextField(blank=True)),
                ('page_status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('private', 'Private')], db_index=True, default='draft', max_length=10)),
                ('page_link_location', models.CharField(choices=[('navbar', 'Navbar'), ('header', 'Header'), ('footer', 'Footer'), ('sidebar', 'Sidebar'), ('unsorted', 'Unsorted')], db_index=True, default='unsorted', max_length=10)),
                ('show_in_position', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('meta_title', models.CharField(blank=True, max_length=200)),
                ('meta_description', models.TextField(blank=True)),
                ('meta_keywords', models.CharField(blank=True, max_length=255)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='cms_content.page')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
                ('slug', models.CharField(db_index=True, max_length=200, unique=True)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('show_in_position', models.BooleanField(default=False)),
                ('page_link_location', models.CharField(choices=[('navbar', 'Navbar'), ('header', 'Header'), ('footer', 'Footer'), ('sidebar', 'Sidebar'), ('unsorted', 'Unsorted')], db_index=True, default='unsorted', max_length=10)),
                ('page_status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('private', 'Private')], db_index=True, default='draft', max_length=10)),
                ('order', models.PositiveIntegerField(default=0)),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='links', to='cms_content.page')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('content', models.TextField(blank=True)),
                ('excerpt', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('private', 'Private')], default='draft', max_length=10)),
                ('views', models.PositiveIntegerField(default=0)),
                ('meta_title', models.CharField(blank=True, max_length=200)),
                ('meta_description', models.TextField(blank=True)),
                ('meta_keywords', models.CharField(blank=True, max_length=255)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
