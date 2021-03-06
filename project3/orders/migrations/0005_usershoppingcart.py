# Generated by Django 3.0.7 on 2020-06-24 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0004_auto_20200622_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_fullname', models.CharField(max_length=255)),
                ('menu_desc', models.CharField(max_length=255)),
                ('menu_portion', models.CharField(max_length=32)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('topping1', models.CharField(blank=True, max_length=32, null=True)),
                ('topping2', models.CharField(blank=True, max_length=32, null=True)),
                ('topping3', models.CharField(blank=True, max_length=32, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppingcart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
