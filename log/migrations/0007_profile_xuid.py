# Generated by Django 2.2.2 on 2019-06-11 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0006_profile_verificationcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='xuid',
            field=models.IntegerField(null=True),
        ),
    ]
