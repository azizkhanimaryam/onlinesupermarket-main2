# Generated by Django 5.1.1 on 2024-09-17 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_category_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='category',
        ),
    ]
