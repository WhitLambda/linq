# Generated by Django 3.0.4 on 2020-04-09 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='yt_username',
            new_name='YT_username',
        ),
    ]