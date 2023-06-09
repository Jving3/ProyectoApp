# Generated by Django 4.0 on 2022-05-25 23:19

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0016_alter_equipo_area_alter_equipo_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='imagen',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, size=[500, 300], upload_to='equipos'),
        ),
        migrations.AlterField(
            model_name='personal',
            name='cargo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='personal',
            name='telefono',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
