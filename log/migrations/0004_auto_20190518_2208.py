# Generated by Django 2.2.1 on 2019-05-18 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0003_entry_enemyship'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='encounterTime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='loss',
            field=models.BooleanField(default=False),
        ),
    ]