# Generated by Django 3.1.3 on 2020-11-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20200925_0613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='imgurl',
            field=models.ImageField(blank=True, default='static/images/omega.png', null=True, upload_to='static/images/products'),
        ),
    ]