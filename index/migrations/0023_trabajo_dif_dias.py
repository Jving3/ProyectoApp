# Generated by Django 3.2.9 on 2022-08-09 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0022_remove_historialherramienta_fecha_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabajo',
            name='dif_dias',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
