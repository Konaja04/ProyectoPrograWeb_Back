# Generated by Django 5.0.2 on 2024-02-19 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend_sals', '0002_alter_actor_name_alter_pelicula_path_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pelicula',
            name='path',
        ),
    ]
