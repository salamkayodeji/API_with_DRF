# Generated by Django 4.1.3 on 2022-11-04 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_name',
            field=models.CharField(default='No Name', max_length=200),
        ),
    ]
