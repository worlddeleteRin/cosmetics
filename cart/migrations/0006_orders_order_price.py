# Generated by Django 3.0.8 on 2020-09-01 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_auto_20200831_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='order_price',
            field=models.IntegerField(default=0, max_length=10),
        ),
    ]
