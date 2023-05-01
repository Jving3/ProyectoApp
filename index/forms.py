
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from index.models import Trabajo, Area, Equipo , Producto, Preventivo, Personal, Empresa ,HistorialPreventivo, HistorialCorrectivo, Herramienta
from datetime import date

TODAY = date.today()

class LoginForm(forms.ModelForm):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'id': 'usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')
    
    
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("El usuario o contraseña son incorrectos")


class EquipoForm(forms.ModelForm):
    class Meta:
        imagen = forms.ImageField()
        model = Equipo
        fields = ('area','codigo', 'descripcion', 'imagen')
        labels = {
            'area': 'Área:',
            'codigo': 'Código: ',
            'imagen': 'Imagen: ',
            'descripcion': 'Descripcion: '
        }

class EditarEquipoForm(forms.ModelForm):

    class Meta:
        imagen = forms.ImageField()
        model = Equipo
        fields = ('area','codigo', 'descripcion', 'imagen')
        labels = {
            'area': 'Área:',
            'codigo': 'Código: ',
            'imagen': 'Imagen: ',
            'descripcion': 'Descripcion: '
        }

        widgets = {
            'area': forms.Select(attrs={'id': 'area_editar'}),
            'codigo': forms.TextInput(attrs={'type': 'text', 'id': 'codigo_editar'}),
            'descripcion': forms.TextInput(attrs={'id': 'descripcion_editar'}),
        }


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ('nombre',)
        labels = {
            'nombre': 'Nombre: ',
        }

class EditarAreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ('nombre',)
        labels = {
            'nombre': 'Nombre: ',
        }
        widgets = {
            'nombre': forms.Select(attrs={'id': 'nombre_area_editar'})
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        imagen = forms.ImageField()
        model = Producto
        fields = ('codigo','descripcion', 'imagen', 'costo','cantidad')
        labels = {
            'codigo': 'Código:',
            'descripcion': 'Descripción: ',
            'imagen': 'Imagen: ',
            'costo': 'Costo $: ',
            'cantidad': 'Cantidad: '
        }

class HerramientaForm(forms.ModelForm):
    class Meta:
        imagen = forms.ImageField()
        model = Herramienta
        fields = ('codigo','descripcion', 'imagen', 'costo','comentarios')
        labels = {
            'codigo': 'Código:',
            'descripcion': 'Descripción: ',
            'imagen': 'Imagen: ',
            'costo': 'Costo $: ',
            'comentarios': 'Comentarios: '
        }
        widgets = {
            'comentarios': forms.Textarea(attrs={'rows': '4'})
        }

class EditarProductoForm(forms.ModelForm):

    class Meta:
        imagen = forms.ImageField()
        model = Producto
        fields = ('codigo', 'descripcion', 'imagen','costo','cantidad')
        labels = {
            'codigo': 'Código:',
            'descripcion': 'Descripción: ',
            'imagen': 'Imagen: ',
            'costo': 'Costo $: ',
            'cantidad': 'Cantidad: '
        }

        widgets = {
            'codigo': forms.TextInput(attrs={'id': 'codigo_editar'}),
            'descripcion': forms.TextInput(attrs={'id': 'descripcion_editar'}),
            'costo': forms.NumberInput(attrs={'id': 'costo_editar'}),
            'cantidad': forms.NumberInput(attrs={'id': 'cantidad_editar'}),
        }



class PreventivoForm(forms.ModelForm):
    class Meta:
        model = Preventivo
        fields = ('equipo','fecha', 'frecuencia', 'actividades','solicitado','estado','responsable', 'subtotalmo', 'supervisadop')
        labels = {
            'equipo': 'Equipo:',
            'fecha': 'Fecha: ',
            'frecuencia': 'Frecuencia (dias): ', 
            'actividades': 'Trabajo a realizar / Trabajo realizado: ',
            'solicitado': 'Solicitado por: ',
            'responsable': 'Asignado a: ',
            'estado': 'Estado: ',
            'subtotalmo': 'Costo Mano Obra $:', 
            'supervisadop': 'Supervisado por:',

        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date' , 'value': TODAY }),
            'actividades': forms.Textarea(attrs={'rows': '4'})
        }
       
class TrabajoForm(forms.ModelForm):
    class Meta:
        model = Trabajo
        fields = ('equipo','fecha', 'actividades', 'solicitadoc', 'estado','responsablec', 'subtotalmo', 'supervisadoc', 'falla', 'file')
        labels = {
            'equipo': 'Equipo:',
            'fecha': 'Fecha: ',
            'actividades': 'Trabajo a realizar / Trabajo realizado: ',
            'solicitadoc': 'Solicitado por: ',
            'responsablec': 'Asignado a: ',
            'estado': 'Estado: ',
            'subtotalmo': 'Costo Mano Obra $:', 
            'supervisadoc': 'Supervisado por:', 
            'falla': 'Descripción de falla:',  
            'file': 'Documentación (PDF):', 
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date' , 'value': TODAY }), 
            'actividades': forms.Textarea(attrs={'rows': '4'}),
            'falla': forms.Textarea(attrs={'rows': '4'}),
        }

class EditarTrabajoForm(forms.ModelForm):
    class Meta:
        model = Trabajo
        fields = ('equipo','fecha','actividades','solicitadoc','estado','responsablec', 'subtotalmo', 'supervisadoc','falla', 'file')
        labels = {
            'equipo': 'Equipo:',
            'fecha': 'Fecha: ',
            'actividades': 'Trabajo a realizar / Trabajo realizado: ',
            'solicitadoc': 'Solicitado por: ',
            'responsablec': 'Asignado a: ',
            'estado': 'Estado: ',
            'subtotalmo': 'Costo Mano Obra $:', 
            'supervisadoc': 'Supervisado por:', 
            'falla': 'Descripción de falla:',  
            'file': 'Documentación (PDF):', 

        }
        widgets = {
            'equipo': forms.Select(attrs={'id': 'equipo_editar'}),
            'fecha': forms.DateInput(attrs={'type': 'date' , 'id': 'fecha_editar'}),
            'actividades': forms.Textarea(attrs={'rows': '4', 'id': 'actividades_editar'}),
            'solicitadoc': forms.Select(attrs={'id': 'solicitadoc_editar'}),
            'estado': forms.Select(attrs={'id': 'estado_editar'}),
            'responsablec': forms.Select(attrs={'id': 'responsablec_editar'}),
            'subtotalmo': forms.NumberInput(attrs={'id': 'subtotalmo_editar'}),
            'supervisadoc': forms.Select(attrs={'id': 'supervisadoc_editar'}),
            'falla': forms.Textarea(attrs={'rows': '4', 'id': 'falla_editar'}),
        }

class HistorialTrabajoForm(forms.ModelForm):
    class Meta:
        model = HistorialCorrectivo
        fields = ('correctivo','fecha_programada','fecha','solicitadohc','supervisadohc','responsablehc', 'subtotalpiezas','subtotalmo','file', 'horas')
        labels = {
            'correctivo': 'OT:',
            'fecha_programada': 'Fecha programada: ',
            'fecha': 'Fecha cierre: ',
            'solicitadohc': 'Solicitado por: ',
            'supervisadohc': 'Supervisado por: ',
            'responsablehc': 'Realizado por: ',
            'subtotalmo': 'Costo Mano Obra $:',
            'subtotalpiezas': 'Costo Materiales $:',
            'file': 'Evidencia PDF: ',
            'horas': 'Horas de paro: ',

        }
        widgets = {
            'correctivo': forms.TextInput(attrs={'id': 'hist_correctivo_editar', 'readonly': 'readonly', 'class': 'bg-info'}),
            'fecha_programada': forms.DateInput(attrs={'type': 'date' , 'id': 'hist_fecha_programada_editar', 'readonly': 'readonly', 'class': 'bg-info'}),
            'fecha': forms.DateInput(attrs={'type': 'date' , 'id': 'hist_fecha_editar', 'value': TODAY}),
            'solicitadohc': forms.Select(attrs={'id': 'hist_solicitadoh'}),
            'supervisadohc': forms.Select(attrs={'id': 'hist_supervisadoh'}),
            'responsablehc': forms.Select(attrs={'id': 'hist_responsable'}),
            'subtotalmo': forms.NumberInput(attrs={'id': 'hist_subtotalmo'}),
            'subtotalpiezas': forms.NumberInput(attrs={'id': 'hist_subtotalpiezas','readonly': 'readonly', 'class': 'bg-info'}),
            'horas': forms.NumberInput(attrs={'id': 'hist_horas'}),
        }

class EditarPreventivoForm(forms.ModelForm):
    class Meta:
        model = Preventivo
        fields = ('equipo','fecha', 'frecuencia', 'actividades','solicitado','estado','responsable', 'subtotalmo', 'supervisadop')
        labels = {
            'equipo': 'Equipo:',
            'fecha': 'Fecha: ',
            'frecuencia': 'Frecuencia (dias): ', 
            'actividades': 'Trabajo a realizar / Trabajo realizado: ',
            'solicitado': 'Solicitado por: ',
            'responsable': 'Asignado a: ',
            'estado': 'Estado: ',
            'subtotalmo': 'Costo Mano Obra $:',
            'supervisadop': 'Supervisado por:',

        }
        widgets = {
            'equipo': forms.Select(attrs={'id': 'equipo_editar'}),
            'fecha': forms.DateInput(attrs={'type': 'date' , 'id': 'fecha_editar'}),
            'frecuencia': forms.NumberInput(attrs={'id': 'frecuencia_editar'}),
            'actividades': forms.Textarea(attrs={'rows': '4', 'id': 'actividades_editar'}),
            'solicitado': forms.Select(attrs={'id': 'solicitado_editar'}),
            'estado': forms.Select(attrs={'id': 'estado_editar'}),
            'responsable': forms.Select(attrs={'id': 'responsable_editar'}),
            'subtotalmo': forms.NumberInput(attrs={'id': 'subtotalmo_editar'}),
            'supervisadop': forms.Select(attrs={'id': 'supervisadop_editar'}),
        }

class HistorialPreventivoForm(forms.ModelForm):
    class Meta:
        model = HistorialPreventivo
        fields = ('preventivo','fecha_programada','fecha','solicitadoh','supervisadoh','responsable', 'subtotalpiezas','subtotalmo','file', 'horas')
        labels = {
            'preventivo': 'Preventivo:',
            'fecha_programada': 'Fecha programada: ',
            'fecha': 'Fecha cierre: ',
            'solicitadoh': 'Solicitado por: ',
            'supervisadoh': 'Supervisado por: ',
            'responsable': 'Realizado por: ',
            'subtotalmo': 'Costo Mano Obra $:',
            'subtotalpiezas': 'Costo Materiales $:',
            'file': 'Evidencia PDF: ',
            'horas': 'Horas de paro: ',

        }
        widgets = {
            'preventivo': forms.TextInput(attrs={'id': 'hist_preventivo_editar', 'readonly': 'readonly', 'class': 'bg-info'}),
            'fecha_programada': forms.DateInput(attrs={'type': 'date' , 'id': 'hist_fecha_programada_editar', 'readonly': 'readonly', 'class': 'bg-info'}),
            'fecha': forms.DateInput(attrs={'type': 'date' , 'id': 'hist_fecha_editar', 'value': TODAY}),
            'solicitadoh': forms.Select(attrs={'id': 'hist_solicitadoh'}),
            'supervisadoh': forms.Select(attrs={'id': 'hist_supervisadoh'}),
            'responsable': forms.Select(attrs={'id': 'hist_responsable'}),
            'subtotalmo': forms.NumberInput(attrs={'id': 'hist_subtotalmo'}),
            'subtotalpiezas': forms.NumberInput(attrs={'id': 'hist_subtotalpiezas','readonly': 'readonly', 'class': 'bg-info'}),
            'horas': forms.NumberInput(attrs={'id': 'hist_horas'}),
        }

class PersonalForm(forms.ModelForm):
    class Meta:
        imagen = forms.ImageField()
        model = Personal
        fields = ('nombre','telefono', 'cargo', 'imagen')
        labels = {
            'nombre': 'Nombre:',
            'telefono': 'Telefono: ',
            'cargo': 'Cargo: ', 
            'imagen': 'Imagen: ',
        }
        
class EditarPersonalForm(forms.ModelForm):

    class Meta:
        imagen = forms.ImageField()
        model = Personal
        fields = ('nombre','telefono', 'cargo', 'imagen')
        labels = {
            'nombre': 'Nombre:',
            'telefono': 'Telefono: ',
            'cargo': 'Cargo: ', 
            'imagen': 'Imagen: ',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'id': 'nombre_editar'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono_editar'}),
            'cargo': forms.TextInput(attrs={'id': 'cargo_editar'}),
        }

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ('nombre','domicilio', 'telefono', 'imagen')
        labels = {
            'nombre': 'Nombre:',
            'telefono': 'Contacto: ',
            'domicilio': 'Domicilio: ', 
            'imagen': 'Imagen: ',
        }


"""
class AccountUpdateForm (forms.ModelForm):
    class Meta:
        model = Account
        fields = ('username', 'imagen', 'about')
        labels = {'username': 'Nombre completo', 'imagen': 'Elige una imagen de perfil', 'about': 'Cuéntanos un poco acerca de ti'}
    
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoestNotExist:
                return username
            raise forms.ValidationError('El usuario "%s" se encuentra actualmente en uso' % username)

"""


