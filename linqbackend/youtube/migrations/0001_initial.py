# Generated by Django 3.0.4 on 2020-04-09 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linq_username', models.CharField(max_length=100)),
                ('yt_username', models.CharField(max_length=100)),
                ('video_id', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=2200)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
    ]