# Generated by Django 2.2.6 on 2019-11-18 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamad2', '0020_auto_20191118_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importedgrant',
            name='amount_awarded',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]