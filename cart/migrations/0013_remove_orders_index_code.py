# Generated by Django 3.0.8 on 2020-09-16 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_orders_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='index_code',
        ),
    ]
