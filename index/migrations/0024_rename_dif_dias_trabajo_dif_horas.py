# Generated by Django 3.2.9 on 2022-08-09 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0023_trabajo_dif_dias'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trabajo',
            old_name='dif_dias',
            new_name='dif_horas',
        ),
    ]
