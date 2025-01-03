# Generated by Django 5.1.1 on 2024-12-22 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopowner', '0002_shop_remove_shopowner_city_remove_shopowner_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopowner',
            name='name',
        ),
        migrations.AddField(
            model_name='shopowner',
            name='first_name',
            field=models.CharField(default='DefaultFirstName', max_length=255, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='shopowner',
            name='last_name',
            field=models.CharField(default='DefaultLastName', max_length=255, verbose_name='Last Name'),
        ),
        migrations.AddField(
            model_name='shopowner',
            name='password',
            field=models.CharField(default='default_password', max_length=255, verbose_name='Password'),
        ),
        migrations.AddField(
            model_name='shopowner',
            name='username',
            field=models.CharField(default='default_user', max_length=255, unique=True, verbose_name='Username'),
        ),
    ]
