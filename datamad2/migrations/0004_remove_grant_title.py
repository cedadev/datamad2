# Generated by Django 2.2.6 on 2019-11-21 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datamad2', '0003_grant_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grant',
            name='title',
        ),
    ]
