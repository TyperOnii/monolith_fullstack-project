# Generated by Django 4.2.20 on 2025-05-21 11:03

import core.apps.users.managers
from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_phone'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', core.apps.users.managers.CustomUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True, verbose_name='Номер телефона пользователя'),
        ),
    ]
