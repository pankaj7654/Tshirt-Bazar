# Generated by Django 3.1.2 on 2020-10-23 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20201023_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='idealfor',
            name='idealFor',
            field=models.CharField(default=0, max_length=20),
        ),
        migrations.AddField(
            model_name='necktype',
            name='neckType',
            field=models.CharField(default=0, max_length=20),
        ),
        migrations.AddField(
            model_name='occasion',
            name='occasion',
            field=models.CharField(default=0, max_length=20),
        ),
        migrations.AlterField(
            model_name='brand',
            name='brand',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name='color',
            name='color',
            field=models.CharField(default=0, max_length=20),
        ),
        migrations.AlterField(
            model_name='sleeve',
            name='sleeve',
            field=models.CharField(default=0, max_length=20),
        ),
    ]
