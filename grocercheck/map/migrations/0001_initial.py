# Generated by Django 3.0.5 on 2020-04-21 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('busyness', models.IntegerField()),
                ('lat', models.CharField(max_length=10)),
                ('lng', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('hours', models.CharField(max_length=10)),
                ('placeID', models.CharField(max_length=100)),
            ],
        ),
    ]
