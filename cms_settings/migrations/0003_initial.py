# Generated by Django 5.1.1 on 2024-10-04 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms_settings', '0002_delete_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('content', models.TextField(blank=True)),
                ('published', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(unique=True)),
                ('meta_title', models.CharField(blank=True, max_length=200)),
                ('meta_description', models.TextField(blank=True)),
                ('meta_keywords', models.CharField(blank=True, max_length=255)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='cms_settings.page')),
            ],
        ),
    ]
