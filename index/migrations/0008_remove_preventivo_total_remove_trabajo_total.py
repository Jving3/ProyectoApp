# Generated by Django 4.0 on 2022-01-28 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_remove_preventivo_fechasiguiente_alter_equipo_imagen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preventivo',
            name='total',
        ),
        migrations.RemoveField(
            model_name='trabajo',
            name='total',
        ),
    ]
