# Generated by Django 5.0.3 on 2024-04-03 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profil',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]
