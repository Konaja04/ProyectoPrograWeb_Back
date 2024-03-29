# Generated by Django 4.2.10 on 2024-02-22 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend_sals', '0009_keyword_user_pelicula_keyword_usuario_keyword'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Formato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Funcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pelicula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.pelicula')),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.IntegerField()),
                ('address', models.CharField(max_length=100)),
                ('second_address', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('path', models.CharField(blank=True, max_length=50, null=True)),
                ('img', models.CharField(blank=True, max_length=200, null=True)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.ciudad')),
            ],
        ),
        migrations.CreateModel(
            name='Ventana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('hour', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.FloatField()),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.genero')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.user')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.FloatField()),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.actor')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.user')),
            ],
        ),
        migrations.CreateModel(
            name='Sala_Formato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.formato')),
                ('sala', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.sala')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asientos', models.CharField(max_length=100)),
                ('funcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.funcion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.user')),
            ],
        ),
        migrations.AddField(
            model_name='funcion',
            name='sala',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.sala'),
        ),
        migrations.AddField(
            model_name='funcion',
            name='ventana',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_sals.ventana'),
        ),
    ]
