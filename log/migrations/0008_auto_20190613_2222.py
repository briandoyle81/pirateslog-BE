# Generated by Django 2.2.2 on 2019-06-13 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0007_profile_xuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='encounterTime',
            field=models.DateTimeField(),
        ),
    ]
