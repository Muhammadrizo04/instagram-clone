# Generated by Django 5.0.3 on 2024-04-02 10:13

import post.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.FileField(upload_to=post.models.user_directory_path, verbose_name='Picture'),
        ),
    ]
