# Generated by Django 3.0.8 on 2020-09-16 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_auto_20200915_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='comment',
            field=models.CharField(default='', max_length=3000),
        ),
    ]
