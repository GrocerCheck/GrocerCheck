# Generated by Django 3.0.5 on 2020-04-26 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_auto_20200426_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='hours',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]