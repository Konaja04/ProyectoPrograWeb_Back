# Generated by Django 4.2.10 on 2024-02-23 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend_sals', '0010_ciudad_formato_funcion_sala_ventana_usuario_genero_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pelicula_Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion', models.FloatField()),
                ('pelicula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.pelicula')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.user')),
            ],
        ),
    ]
