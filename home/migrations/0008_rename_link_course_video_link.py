# Generated by Django 4.1.7 on 2023-04-05 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_course_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='link',
            new_name='video_link',
        ),
    ]
