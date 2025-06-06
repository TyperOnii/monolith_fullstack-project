# Generated by Django 4.2.20 on 2025-05-25 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_projectservice_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='projects',
        ),
        migrations.AddField(
            model_name='project',
            name='services',
            field=models.ManyToManyField(related_name='projects', through='projects.ProjectService', to='projects.service'),
        ),
        migrations.AlterModelTable(
            name='service',
            table='Service',
        ),
    ]
