# Generated by Django 3.0.8 on 2020-07-25 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20200725_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
    ]
