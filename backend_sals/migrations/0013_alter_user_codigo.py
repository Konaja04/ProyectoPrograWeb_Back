# Generated by Django 4.2.10 on 2024-02-24 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_sals', '0012_user_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='codigo',
            field=models.IntegerField(),
        ),
    ]
