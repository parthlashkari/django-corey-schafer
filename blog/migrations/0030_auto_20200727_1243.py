# Generated by Django 3.0.8 on 2020-07-27 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_auto_20200726_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='default1.jpg', null=True, upload_to='profile_pics'),
        ),
    ]
