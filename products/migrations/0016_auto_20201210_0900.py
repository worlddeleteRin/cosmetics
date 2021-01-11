# Generated by Django 3.1.3 on 2020-12-10 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20201210_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pr_destination',
            field=models.ManyToManyField(blank=True, default=None, to='products.Destination'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pr_hairtype',
            field=models.ManyToManyField(blank=True, default=None, to='products.Hairtype'),
        ),
    ]