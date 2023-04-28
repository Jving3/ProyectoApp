
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django_resized import ResizedImageField

TODAY = date.today()
# Create your models here.

ESTADOS = ( 
    ("Programado", "Programado"), 
    ("En espera", "En espera"), 
    ("En proceso", "En proceso"), 
    ("Atrasado", "Atrasado"),  
    ("Realizado", "Realizado")
    )


def validate_image(imagen):
    max_height = 100
    max_width = 100
    height = imagen.height 
    width = imagen.width
    if width > max_width or height > max_height:
        raise ValidationError("El largo de la imagen no debe superar los {} px y ancho de la imagen no deben superar los {} px".format(max_height, max_width))


def validate_image_equipo(imagen):
    max_height = 300
    max_width = 400
    height = imagen.height 
    width = imagen.width
    if width > max_width or height > max_height:
        raise ValidationError("El largo de la imagen no debe superar los {} px y ancho de la imagen no deben superar los {} px".format(max_height, max_width))


class Personal (models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    cargo = models.CharField(max_length=255, null=True, blank=True)
    imagen = models.ImageField(upload_to='personal', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='tecnico'
        verbose_name_plural = 'tecnicos'
    
    def __str__(self):
        return self.nombre


class Area (models.Model):
    nombre = models.CharField(max_length=255)


    class Meta:
        verbose_name='area'
        verbose_name_plural = 'areas'
    
    def __str__(self):
        return self.nombre


class Equipo (models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=255, null=True, blank = True)
    descripcion =  models.CharField(max_length=255, unique=True, null=False)
    imagen = ResizedImageField(size=[400, 300], upload_to='equipos', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='equipo'
        verbose_name_plural = 'equipos'
    
    def __str__(self):
        return self.descripcion
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['imagen', 'created', 'updated'])
        return item

class Producto (models.Model):
    codigo = models.CharField(max_length=255, unique=True, null=True, blank = True)
    descripcion =  models.CharField(max_length=255, unique=True, null=False)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)
    costo = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    cantidad = models.DecimalField(max_digits=15, decimal_places=2 , null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='producto'
        verbose_name_plural = 'productos'
        order_with_respect_to = 'descripcion'
    
    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['imagen', 'created', 'updated'])
        return item

class Herramienta (models.Model):
    codigo = models.CharField(max_length=255, unique=True, null=True, blank = True)
    descripcion =  models.CharField(max_length=255, unique=True, null=False)
    imagen = models.ImageField(upload_to='herramientas', null=True, blank=True)
    costo = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    comentarios = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='herramienta'
        verbose_name_plural = 'herramientas'
    
    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['imagen', 'created', 'updated'])
        return item

class Preventivo (models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha = models.DateField(max_length=255)
    fecha_str = str(fecha)
    frecuencia = models.IntegerField(null=False)
    actividades = models.TextField(blank=False)
    herramientas = models.TextField(blank=True, null=True)
    solicitado = models.ForeignKey(Personal, on_delete=models.SET_NULL , null=True , related_name='solicitado')
    responsable = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True)
    supervisadop = models.ForeignKey(Personal, on_delete=models.SET_NULL , null=True, related_name='supervisadop')
    subtotalpiezas = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    subtotalmo = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    estado = models.CharField(max_length=255, choices = ESTADOS, default='Programado', null=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True , null=True)

    class Meta:
        verbose_name='preventivo'
        verbose_name_plural = 'preventivos'
        order_with_respect_to = 'fecha'
    
    def __str__(self):
        return str(self.id)

class HistorialPreventivo(models.Model):
    preventivo = models.ForeignKey(Preventivo, on_delete=models.CASCADE)
    fecha = models.DateField(max_length=255)
    fecha_programada = models.DateField(max_length=255, null=True)
    solicitadoh = models.ForeignKey(Personal, on_delete=models.SET_NULL , null=True , related_name='solicitadoh')
    responsable = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True)
    supervisadoh = models.ForeignKey(Personal, on_delete=models.SET_NULL , null=True , related_name='supervisadoh')
    subtotalpiezas = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    subtotalmo = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    horas = models.IntegerField(null=True, default=0)
    file = models.FileField(null=True, upload_to='preventivos', blank=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='historial preventivo'
        verbose_name_plural = 'historial preventivos'
        order_with_respect_to = 'created'
    
    def __str__(self):
        return self.created

class ProductosPreventivo(models.Model):
    preventivo = models.ForeignKey(Preventivo, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=13, decimal_places=2 , null=False)
    precio = models.DecimalField(max_digits=13, decimal_places=2 , null=False , default=0)
    subtotal = models.DecimalField(max_digits=13, decimal_places=2 , null=False , default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='producto preventivo'
        verbose_name_plural = 'productos preventivo'
        order_with_respect_to = 'created'
    
    def __str__(self):
        return self.producto


class Trabajo(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha = models.DateField(max_length=255)
    fecha_str = str(fecha)
    actividades = models.TextField(blank=False)
    herramientas = models.TextField(blank=True, null=True)
    solicitadoc = models.ForeignKey(Personal, on_delete=models.SET_NULL , null=True , related_name='solicitadoc')
    responsablec = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, related_name='responsablec')
    supervisadoc = models.ForeignKey(Personal, on_delete=models.SET_NULL , null=True, related_name='supervisadoc')
    subtotalpiezas = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    subtotalmo = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    estado = models.CharField(max_length=255, choices = ESTADOS, default='Programado', null=False)
    falla = models.TextField(null=True)
    file = models.FileField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True , null=True)
    dif_horas = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        verbose_name='correctivo'
        verbose_name_plural = 'correctivos'
    
    def __str__(self):
        return self.equipo


class ProductosTrabajo(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=13, decimal_places=2 , null=False)
    precio = models.DecimalField(max_digits=13, decimal_places=2 , null=False , default=0)
    subtotal = models.DecimalField(max_digits=13, decimal_places=2 , null=False, default=0)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='producto trabajo'
        verbose_name_plural = 'productos trabajo'
    
    def __str__(self):
        return self.producto

class HistorialCorrectivo(models.Model):
    correctivo = models.ForeignKey(Trabajo, on_delete=models.CASCADE)
    fecha = models.DateField(max_length=255)
    fecha_programada = models.DateField(max_length=255, null=True)
    solicitadohc = models.ForeignKey(Personal, on_delete=models.SET_NULL , null=True , related_name='solicitadohc')
    responsablehc = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True,  related_name='responsablehc')
    supervisadohc = models.ForeignKey(Personal, on_delete=models.SET_NULL , null=True , related_name='supervisadohc')
    subtotalpiezas = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    subtotalmo = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    horas = models.IntegerField(null=True, default=0)
    file = models.FileField(null=True, upload_to='correctivos', blank=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='historial correctivo'
        verbose_name_plural = 'historial correctivos'
        order_with_respect_to = 'created'
    
    def __str__(self):
        return self.created

class Empresa (models.Model):
    nombre = models.CharField(max_length=255)
    domicilio = models.CharField(max_length=255, null=True)
    telefono = models.CharField(max_length=255, null=True)
    imagen = ResizedImageField(size=[100, 100], upload_to='empresa', blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='empresa'
        verbose_name_plural = 'empresa'
    
    def __str__(self):
        return self.nombre

class HistorialHerramienta(models.Model):
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE , null=True, blank=True)
    preventivo = models.ForeignKey(Preventivo, on_delete=models.CASCADE , null=True, blank=True)
    correctivo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='historial herramienta'
        verbose_name_plural = 'historial herramientas'
    
    def __str__(self):
        return self.created