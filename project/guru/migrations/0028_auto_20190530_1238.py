# Generated by Django 2.1.4 on 2019-05-30 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guru', '0027_auto_20190522_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentlike',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='commentlike',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='connection',
            name='sec_id',
        ),
        migrations.RemoveField(
            model_name='connection',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='mentee',
            name='user',
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='mentees',
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='user',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='postcomment',
            name='post',
        ),
        migrations.RemoveField(
            model_name='postcomment',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='postlike',
            name='post',
        ),
        migrations.RemoveField(
            model_name='postlike',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='CommentLike',
        ),
        migrations.DeleteModel(
            name='Connection',
        ),
        migrations.DeleteModel(
            name='Mentee',
        ),
        migrations.DeleteModel(
            name='Mentor',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='PostComment',
        ),
        migrations.DeleteModel(
            name='PostLike',
        ),
    ]
