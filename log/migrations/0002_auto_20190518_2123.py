# Generated by Django 2.2.1 on 2019-05-18 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Crewmate',
        ),
        migrations.AlterField(
            model_name='entry',
            name='ship',
            field=models.CharField(choices=[('U', 'Unknown'), ('S', 'Sloop'), ('B', 'Brig'), ('G', 'Galleon')], default='U', max_length=10),
        ),
        migrations.AlterField(
            model_name='entry',
            name='tears',
            field=models.CharField(choices=[('U', 'Unknown'), ('L', 'Low'), ('M', 'Medium'), ('H', 'High'), ('E', 'Extraordinary')], default='U', max_length=10),
        ),
        migrations.AlterField(
            model_name='entry',
            name='treasure',
            field=models.CharField(choices=[('U', 'Unknown'), ('L', 'Low'), ('M', 'Medium'), ('H', 'High'), ('E', 'Extraordinary')], default='U', max_length=10),
        ),
        migrations.AlterField(
            model_name='island',
            name='name',
            field=models.CharField(default='At Sea', max_length=50),
        ),
    ]
