# Generated by Django 3.1.2 on 2020-12-22 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_tshirt_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tshirt',
            name='slug',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
