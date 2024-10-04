# Generated by Django 5.1.1 on 2024-10-04 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_content', '0004_alter_page_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='order',
            field=models.PositiveIntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
