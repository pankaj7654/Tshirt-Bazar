# Generated by Django 3.1.2 on 2020-12-22 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_sizevariant'),
    ]

    operations = [
        migrations.AddField(
            model_name='tshirt',
            name='slug',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
