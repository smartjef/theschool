# Generated by Django 3.2.5 on 2021-07-20 12:34

import app_users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0005_alter_user_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='profile_Pic',
            field=models.ImageField(default='undraw_profile.svg', upload_to=app_users.models.path_and_rename, verbose_name='Profile Picture'),
        ),
    ]
