# Generated by Django 3.0.8 on 2020-09-15 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_auto_20200915_2123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='promo',
        ),
        migrations.AddField(
            model_name='cart',
            name='promo',
            field=models.ManyToManyField(to='cart.Promocode'),
        ),
    ]
