# Generated by Django 2.2.13 on 2020-06-11 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamad2', '0017_merge_20200521_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='download_title',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]