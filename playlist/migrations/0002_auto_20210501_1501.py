# Generated by Django 3.1.7 on 2021-05-01 20:01

from django.db import migrations, models
import django.db.models.deletion
import playlist.models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tvshowtemporadaproxy',
            options={'verbose_name': 'Temporada', 'verbose_name_plural': 'Temporadas'},
        ),
        migrations.CreateModel(
            name='PlayListRelacionado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlist.playlist')),
                ('relacionado', models.ForeignKey(limit_choices_to=playlist.models.pr_opcion_limite, on_delete=django.db.models.deletion.CASCADE, related_name='item_relacionado', to='playlist.playlist')),
            ],
        ),
    ]
