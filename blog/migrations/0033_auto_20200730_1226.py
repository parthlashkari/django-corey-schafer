# Generated by Django 3.0.8 on 2020-07-30 06:56

import blog.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0032_post_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='profile_vids', validators=[blog.validators.validate_file_size]),
        ),
    ]
