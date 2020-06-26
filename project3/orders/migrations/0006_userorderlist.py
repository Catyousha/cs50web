# Generated by Django 3.0.7 on 2020-06-25 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0005_usershoppingcart'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOrderList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_fullname', models.CharField(max_length=255)),
                ('order_desc', models.TextField()),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('user_address', models.TextField()),
                ('order_status', models.CharField(choices=[('1', 'Waiting'), ('2', 'Cooking'), ('3', 'Delivering'), ('4', 'Complete')], max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
