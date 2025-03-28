# Generated by Django 5.1.7 on 2025-03-26 06:03

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_alter_category_id_alter_feedback_id_alter_like_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=85, scale=None, size=[800, 600], upload_to='recipes/'),
        ),
    ]
