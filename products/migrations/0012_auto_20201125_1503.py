# Generated by Django 3.1.3 on 2020-11-25 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20201125_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='imgurl',
            field=models.ImageField(blank=True, default='omega.png', null=True, upload_to='static/images/products'),
        ),
    ]
