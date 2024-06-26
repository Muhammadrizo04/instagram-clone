# Generated by Django 5.0.3 on 2024-04-04 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0004_alter_profil_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='profil',
            name='username',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
