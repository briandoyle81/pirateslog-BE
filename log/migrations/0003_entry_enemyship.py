# Generated by Django 2.2.1 on 2019-05-18 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0002_auto_20190518_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='enemyShip',
            field=models.CharField(choices=[('U', 'Unknown'), ('S', 'Sloop'), ('B', 'Brig'), ('G', 'Galleon')], default='U', max_length=10),
        ),
    ]
