# Generated by Django 3.0.8 on 2020-07-25 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_auto_20200725_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='default1.jpg', null=True, upload_to='profile_pics'),
        ),
    ]
