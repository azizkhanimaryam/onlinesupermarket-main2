# Generated by Django 5.1.1 on 2024-09-18 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_stock_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='image',
        ),
    ]
