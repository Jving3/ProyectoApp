# Generated by Django 4.0 on 2022-01-11 03:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'area',
                'verbose_name_plural': 'areas',
            },
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('descripcion', models.CharField(max_length=255, unique=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='productos')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='index.area')),
            ],
            options={
                'verbose_name': 'equipo',
                'verbose_name_plural': 'equipos',
            },
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=255, null=True)),
                ('cargo', models.CharField(max_length=255, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='personal')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'tecnico',
                'verbose_name_plural': 'tecnicos',
            },
        ),
        migrations.CreateModel(
            name='Preventivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(max_length=255)),
                ('frecuencia', models.IntegerField()),
                ('actividades', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.equipo')),
            ],
            options={
                'verbose_name': 'preventivo',
                'verbose_name_plural': 'preventivos',
                'order_with_respect_to': 'fecha',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('descripcion', models.CharField(max_length=255, unique=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='productos')),
                ('costo', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'producto',
                'verbose_name_plural': 'productos',
                'order_with_respect_to': 'descripcion',
            },
        ),
        migrations.CreateModel(
            name='Trabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(max_length=255)),
                ('realizado', models.BooleanField(default=False)),
                ('actividades', models.TextField()),
                ('subtotalpiezas', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('subtotalmo', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.equipo')),
                ('responsable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.personal')),
            ],
            options={
                'verbose_name': 'trabajo',
                'verbose_name_plural': 'trabajos',
            },
        ),
        migrations.CreateModel(
            name='ProductosTrabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.producto')),
                ('trabajo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.trabajo')),
            ],
            options={
                'verbose_name': 'producto trabajo',
                'verbose_name_plural': 'productos trabajo',
            },
        ),
        migrations.CreateModel(
            name='ProductosPreventivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('preventivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.preventivo')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.producto')),
            ],
            options={
                'verbose_name': 'producto preventivo',
                'verbose_name_plural': 'productos preventivo',
                'order_with_respect_to': 'created',
            },
        ),
    ]
