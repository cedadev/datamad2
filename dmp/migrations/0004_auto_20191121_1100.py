# Generated by Django 2.2.6 on 2019-11-21 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dmp', '0003_auto_20191121_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='sciSupContact2',
            field=models.ForeignKey(blank=True, help_text='Data centre contact for this Project', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sciSupContact2s', to='dmp.Person'),
        ),
    ]
