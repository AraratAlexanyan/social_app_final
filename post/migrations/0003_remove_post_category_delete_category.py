# Generated by Django 4.1.5 on 2023-01-28 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_remove_post_post_name_alter_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]