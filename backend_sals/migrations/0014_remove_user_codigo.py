# Generated by Django 4.2.10 on 2024-02-24 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend_sals', '0013_alter_user_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='codigo',
        ),
    ]