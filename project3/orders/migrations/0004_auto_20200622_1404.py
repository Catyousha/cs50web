# Generated by Django 3.0.7 on 2020-06-22 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20200622_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalsubs',
            name='large',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='additionalsubs',
            name='small',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]
