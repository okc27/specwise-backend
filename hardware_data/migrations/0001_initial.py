# Generated by Django 5.1.1 on 2024-12-23 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.CharField(blank=True, max_length=255, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('link', models.URLField(unique=True)),
            ],
        ),
    ]
