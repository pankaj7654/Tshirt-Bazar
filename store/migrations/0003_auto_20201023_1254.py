# Generated by Django 3.1.2 on 2020-10-23 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20201023_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='brand',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='color',
            name='color',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='sleeve',
            name='sleeve',
            field=models.CharField(max_length=20),
        ),
    ]