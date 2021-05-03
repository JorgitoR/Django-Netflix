# Generated by Django 3.1.7 on 2021-05-01 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0003_playlist_relacionados'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='relacionados',
            field=models.ManyToManyField(blank=True, related_name='_playlist_relacionados_+', through='playlist.PlayListRelacionado', to='playlist.PlayList'),
        ),
    ]