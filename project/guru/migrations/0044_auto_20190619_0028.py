# Generated by Django 2.1.4 on 2019-06-19 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guru', '0043_auto_20190619_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
