# Generated by Django 3.1.3 on 2020-12-10 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_product_pr_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pr_destination',
            field=models.ManyToManyField(default=None, to='products.Destination'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pr_hairtype',
            field=models.ManyToManyField(default=None, to='products.Hairtype'),
        ),
    ]