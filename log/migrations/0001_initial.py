# Generated by Django 2.2.3 on 2019-07-12 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('myShip', models.CharField(choices=[('U', 'Unknown'), ('S', 'Sloop'), ('B', 'Brig'), ('G', 'Galleon'), ('K', 'Karen'), ('M', 'Meg'), ('SK', 'Skelleon'), ('F', 'Fort'), ('SC', 'Ship Cloud')], default='U', max_length=10)),
                ('enemyShip', models.CharField(choices=[('U', 'Unknown'), ('S', 'Sloop'), ('B', 'Brig'), ('G', 'Galleon'), ('K', 'Karen'), ('M', 'Meg'), ('SK', 'Skelleon'), ('F', 'Fort'), ('SC', 'Ship Cloud')], default='U', max_length=10)),
                ('loss', models.BooleanField(default=False)),
                ('treasure', models.CharField(choices=[('U', 'Unknown'), ('N', 'None'), ('L', 'Low'), ('M', 'Medium'), ('H', 'High'), ('E', 'Extraordinary')], default='U', max_length=10)),
                ('tears', models.CharField(choices=[('U', 'Unknown'), ('N', 'None'), ('L', 'Low'), ('M', 'Medium'), ('H', 'High'), ('E', 'Extraordinary')], default='U', max_length=10)),
                ('enemyCrewSize', models.IntegerField()),
                ('content', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('encounterTime', models.DateTimeField()),
                ('videoURL', models.URLField(default='http://www.youtube.com', verbose_name='URL')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('map_location', models.CharField(default='Unknown', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Island',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='At Sea', max_length=50)),
                ('location', models.CharField(default='Unknown', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserLogEntry',
            fields=[
                ('entry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='log.Entry')),
            ],
            bases=('log.entry',),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('gamertag', models.CharField(max_length=15)),
                ('xuid', models.IntegerField(null=True)),
                ('verified', models.BooleanField(default=False)),
                ('verificationCode', models.CharField(max_length=6)),
                ('friends', models.ManyToManyField(blank=True, related_name='myFriends', to='log.Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='log.Profile'),
        ),
        migrations.AddField(
            model_name='entry',
            name='crew',
            field=models.ManyToManyField(related_name='crewNames', to='log.Profile'),
        ),
        migrations.AddField(
            model_name='entry',
            name='island',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='islandName', to='log.Island'),
        ),
    ]
