# Generated by Django 3.0.8 on 2020-09-15 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20200909_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_rate',
            field=models.IntegerField(default=0),
        ),
    ]
