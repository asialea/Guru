# Generated by Django 2.1.4 on 2019-05-21 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guru', '0015_auto_20190519_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avi_path',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
