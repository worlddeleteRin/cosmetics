# Generated by Django 3.0.8 on 2020-09-25 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_remove_orders_index_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='imgurl',
            field=models.ImageField(upload_to='static/images/products'),
        ),
    ]
