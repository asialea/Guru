# Generated by Django 2.1.4 on 2019-05-22 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guru', '0024_avi_signature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avi',
            name='delete_token',
        ),
        migrations.RemoveField(
            model_name='avi',
            name='signature',
        ),
    ]
