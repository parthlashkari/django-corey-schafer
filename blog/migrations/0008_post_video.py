# Generated by Django 3.0.8 on 2020-07-25 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_remove_post_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(null=True, upload_to='profile_vids', verbose_name=''),
        ),
    ]
