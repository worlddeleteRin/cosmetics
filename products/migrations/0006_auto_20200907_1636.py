# Generated by Django 3.0.8 on 2020-09-07 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20200825_0536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='imgurl',
            field=models.CharField(default='https://placehold.it/300x300', max_length=1000),
        ),
    ]
