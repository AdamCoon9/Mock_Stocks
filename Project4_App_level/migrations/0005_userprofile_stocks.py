# Generated by Django 5.0.6 on 2024-06-22 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project4_App_level', '0004_userprofile_bio_userprofile_birth_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='stocks',
            field=models.ManyToManyField(blank=True, related_name='stocks', to='Project4_App_level.stock'),
        ),
    ]
