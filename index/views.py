
from django.shortcuts import render , redirect
from django.contrib.auth import login, authenticate, logout
from index.forms import TODAY , LoginForm , TrabajoForm , EquipoForm , EditarEquipoForm , AreaForm , EditarAreaForm , ProductoForm, EditarProductoForm, PreventivoForm , PersonalForm, EditarPersonalForm, EmpresaForm, EditarPreventivoForm, HistorialPreventivoForm, EditarTrabajoForm, HistorialTrabajoForm, HerramientaForm
from django.contrib.auth.decorators import login_required
#from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q , Avg
from index.models import Herramienta, Trabajo , Equipo , Area, Equipo, Producto, Preventivo, Personal, Empresa , ProductosPreventivo, HistorialPreventivo, ProductosTrabajo, HistorialCorrectivo , HistorialHerramienta
from django.http import JsonResponse , HttpResponse
from itertools import groupby
from datetime import date, datetime , timedelta
from django.template.loader import render_to_string
from django.views.generic import ListView
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from django.utils.decorators import method_decorator
HOY = datetime.today().strftime('%Y-%m-%d')
import os
import json
#from django.core import serializers
from django.utils.dateparse import parse_date

# Create your views here.
def login_view(request):
    
    user = request.user

    if user.is_authenticated:
        return redirect('Index')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect ('Index')
    else:
        form = LoginForm()

    context = {'form': form}
    
    return render(request, 'login.html', context)



@login_required(login_url='Login')
def correctivos_view(request):
    
    form_add = TrabajoForm()
    form_editar = EditarTrabajoForm()
    form_historial = HistorialTrabajoForm()
    correctivos = Trabajo.objects.all()
    num_programado = len(Trabajo.objects.filter(estado="Programado")) 
    num_espera = len(Trabajo.objects.filter(estado="En espera")) 
    num_proceso = len(Trabajo.objects.filter(estado="En proceso"))
    num_atrasado = len(Trabajo.objects.filter(estado="Atrasado"))
    num_realizado = len(Trabajo.objects.filter(estado="Realizado"))
    herramientas = Herramienta.objects.all()
    context = {
        'form_add': form_add,
        'num_programado': num_programado,
        'num_espera': num_espera,
        'num_proceso': num_proceso,
        'num_atrasado': num_atrasado,
        'num_realizado': num_realizado,
        'correctivos': correctivos,
        'form_editar': form_editar,
        'form_historial': form_historial,
        'herramientas': herramientas
    }

    return render(request, 'correctivos.html', context)

@login_required(login_url='Login')
def add_correctivo_view(request):
    if request.POST:
        #print(request.POST)
        form = TrabajoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                num_trabajos = float(Trabajo.objects.all().count())
                #print(num_trabajos)
                if num_trabajos >= 2:
                    last = Trabajo.objects.latest('id')
                    trabajos = Trabajo.objects.filter(equipo=last.equipo).order_by("-id")
                    actual = trabajos[0].created
                    previo = trabajos[1].created
                    delta = actual - previo
                    horas = round(float(delta.seconds) / 3600,2)
                    last.dif_horas = horas
                    last.save()
                
            except:
                messages.warning(request,"Correctivo no agregado")
                return redirect('Index')


    return redirect('Index')

@login_required(login_url='Login')
def edit_correctivo_view(request):
    if request.POST:
        correctivo = Trabajo.objects.get(pk=request.POST.get('id_correctivo_editar'))
        form = EditarTrabajoForm(
            request.POST, request.FILES, instance=correctivo)
        if form.is_valid():
            form.save()

    return redirect('Index')

@login_required(login_url='Login')
def delete_correctivo_view(request):
    if request.POST:
        correctivo = Trabajo.objects.get(pk=request.POST.get('id_correctivo_eliminar'))
        correctivo.delete()
        
    return redirect('Index')

@login_required(login_url='Login')
def add_historial_correctivo_view(request):
    if request.POST:
        #print(request.POST)
        form = HistorialTrabajoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                correctivo = Trabajo.objects.get(pk=request.POST.get('correctivo'))
                correctivo.estado = 'Realizado'
                correctivo.save()
                #Quitar anteriores
                historicos = HistorialCorrectivo.objects.filter(correctivo=correctivo)
                historicos.delete()
                #Dar de baja productos del historial
                productos_correctivo = ProductosTrabajo.objects.filter(trabajo=request.POST.get('correctivo'))
                for i in productos_correctivo:
                    obtain_product = Producto.objects.get(pk=i.producto.id)
                    suma = float(obtain_product.cantidad) - float(i.cantidad)
                    obtain_product.cantidad = suma
                    obtain_product.save()
                #Guardar Formulario

                form.save()
            except Exception as e:
                messages.warning(request, str(e))
                return redirect('Index')
        else:
            messages.warning(request,'Hubo un error con el formulario')

    return redirect('Index')

@login_required(login_url='Login')
def export_pdf_correctivo_view(request, id):
    id_int = int(id)
    correctivo = Trabajo.objects.get(pk=id_int)
    empresa = Empresa.objects.get(pk=1)
    productos_correctivo = ProductosTrabajo.objects.filter(trabajo=id_int)

    context = {
        'correctivo': correctivo,
        'empresa': empresa,
        'productos': productos_correctivo
    }
    html = render_to_string("pdf_correctivo.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"

    font_config = FontConfiguration()
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)

    return response

def logout_view(request):
    logout(request)
    return redirect('Login')

@login_required(login_url='Login')
def equipos_view(request):

    form_equipo = EquipoForm()
    form_editar_equipo = EditarEquipoForm()
    form_area = AreaForm()
    form_editar_area = EditarAreaForm()
    equipos = Equipo.objects.all()
    areas = Area.objects.all()
    num_equipos = len(equipos)

    context = {
        'form_equipo': form_equipo,
        'form_editar_equipo': form_editar_equipo,
        'equipos': equipos,
        'areas': areas,
        'num_equipos': num_equipos, 
        'form_area': form_area,
        'form_editar_area': form_editar_area,
    }
    return render(request, 'equipos.html', context)

@login_required(login_url='Login')
def add_equipo_view(request):
    if request.POST:
        form = EquipoForm(request.POST, request.FILES)
        if form.is_valid():
             instance = form.save()
             instance.save()

    return redirect('Equipos')


@login_required(login_url='Login')
def edit_equipo_view(request):
    if request.POST:
        equipo = Equipo.objects.get(pk=request.POST.get('id_equipo_editar'))
        form = EditarEquipoForm(
            request.POST, request.FILES, instance=equipo)
        if form.is_valid:
            if equipo.imagen:
                os.remove(equipo.imagen.path)
            form.save()

    return redirect('Equipos')

@login_required(login_url='Login')
def delete_equipo_view(request):
    if request.POST:
        equipo = Equipo.objects.get(pk=request.POST.get('id_equipo_eliminar'))
        if equipo.imagen:
            os.remove(equipo.imagen.path)
        equipo.delete()
        
    return redirect('Equipos')


@login_required(login_url='Login')
def add_area_view(request):
    if request.POST:
        form = AreaForm(request.POST)
        if form.is_valid:
             instance = form.save()
             instance.save()


    return redirect('Equipos')

@login_required(login_url='Login')
def delete_area_view(request):
    if request.POST:
        area = Area.objects.get(pk=request.POST.get('id_area_eliminar'))
        area.delete()
        
    return redirect('Equipos')

@login_required(login_url='Login')
def inventario_view(request):
    
    form_producto = ProductoForm()
    form_editar_producto = EditarProductoForm()
    productos = Producto.objects.all()
    num_productos = len(productos)

    context = {
        'form_producto': form_producto,
        'form_editar_producto': form_editar_producto,
        'productos': productos,
        'num_productos': num_productos
    }
    return render(request, 'inventario.html', context)

@login_required(login_url='Login')
def herramientas_view(request):
    
    form_producto = HerramientaForm()
    productos = Herramienta.objects.all()
    num_productos = len(productos)
    historial = HistorialHerramienta.objects.all()

    context = {
        'form_producto': form_producto,
        'productos': productos,
        'num_productos': num_productos,
        'historial': historial
    }
    return render(request, 'herramientas.html', context)


@login_required(login_url='Login')
def delete_herramienta_view(request):
    if request.POST:
        producto = Herramienta.objects.get(pk=request.POST.get('id_producto_eliminar'))
        if producto.imagen:
            os.remove(producto.imagen.path)
        producto.delete()
        
    return redirect('Herramientas')

@login_required(login_url='Login')
def delete_producto_view(request):
    if request.POST:
        producto = Producto.objects.get(pk=request.POST.get('id_producto_eliminar'))
        if producto.imagen:
            os.remove(producto.imagen.path)
        producto.delete()
        
    return redirect('Product')

@login_required(login_url='Login')
def add_herramienta_view(request):
    if request.POST:
        #print(request.POST)
        form = HerramientaForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages.warning(request,"Herramienta ya agregada o datos incorrectos")
                return redirect('Herramientas')


    return redirect('Herramientas')

@login_required(login_url='Login')
def add_product_view(request):
    if request.POST:
        #print(request.POST)
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages.warning(request,"Producto ya agregado o datos incorrectos")
                return redirect('Product')


    return redirect('Product')


@login_required(login_url='Login')
def edit_product_view(request):
    if request.POST:
        producto = Producto.objects.get(pk=request.POST.get('id_producto_editar'))
        form = EditarProductoForm(
            request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()

    return redirect('Product')


@login_required(login_url='Login')
def preventivos_view(request, data=1):
     
    form_add = PreventivoForm()
    if int(data) == 1:
        preventivos = Preventivo.objects.all()
    elif int(data) == 2:
        preventivos = Preventivo.objects.filter(fecha=HOY)
    elif int(data) == 3:
        preventivos = Preventivo.objects.filter(~Q(estado="Realizado") and Q(fecha__lt = HOY))

    form_editar = EditarPreventivoForm()
    form_historial = HistorialPreventivoForm()
    herramientas = Herramienta.objects.all()
    context = {
        'form_add': form_add,
        'form_editar': form_editar,
        'form_historial': form_historial,
        'hoy': TODAY,
        'preventivos': preventivos,
        'herramientas': herramientas
    }

    return render(request, 'preventivos.html', context)

@login_required(login_url='Login')
def add_preventivo_view(request):
    if request.POST:
        #print(request.POST)
        form = PreventivoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
            except:
                messages.warning(request,"Preventivo no agregado")
                return redirect('Preventivos')


    return redirect('Preventivos')

@login_required(login_url='Login')
def edit_preventivo_view(request):
    if request.POST:
        preventivo = Preventivo.objects.get(pk=request.POST.get('id_preventivo_editar'))
        form = EditarPreventivoForm(
            request.POST, request.FILES, instance=preventivo)
        if form.is_valid():
            form.save()

    return redirect('Preventivos')

@login_required(login_url='Login')
def delete_preventivo_view(request):
    if request.POST:
        preventivo = Preventivo.objects.get(pk=request.POST.get('id_preventivo_eliminar'))
        preventivo.delete()
        
    return redirect('Preventivos')


@login_required(login_url='Login')
def personal_view(request):
    
    form_personal = PersonalForm()
    form_editar_personal = EditarPersonalForm()
    personal = Personal.objects.all()
    num_personal = len(personal)

    context = {
        'form_personal': form_personal,
        'form_editar_personal': form_editar_personal,
        'personal': personal,
        'num_personal': num_personal
    }
    return render(request, 'personal.html', context)


@login_required(login_url='Login')
def add_personal_view(request):
    if request.POST:
        #print(request.POST)
        form = PersonalForm(request.POST, request.FILES)
        if form.is_valid():
            print("Si llegamos hasta aqui")
            try:
                form.save()
            except:
                messages.warning(request,"Personal ya agregado o datos incorrectos")
                return redirect('Personal')


    return redirect('Personal')


@login_required(login_url='Login')
def edit_personal_view(request):
    if request.POST:
        producto = Personal.objects.get(pk=request.POST.get('id_personal_editar'))
        form = EditarPersonalForm(
            request.POST, request.FILES, instance=producto)
        if form.is_valid:
            form.save()

    return redirect('Personal')


@login_required(login_url='Login')
def delete_personal_view(request):
    if request.POST:
        personal = Personal.objects.get(pk=request.POST.get('id_personal_eliminar'))
        if personal.imagen:
            os.remove(personal.imagen.path)
        personal.delete()
        
    return redirect('Personal')

@login_required(login_url='Login')
def empresa_view(request):
    empresa = Empresa.objects.get(pk=1)
    form_empresa = EmpresaForm(instance=empresa)

    if request.POST:
        empresa = Empresa.objects.get(pk=1)
        form_empresa = EmpresaForm(
            request.POST, request.FILES, instance=empresa)
        if form_empresa.is_valid():
            """
            if form_empresa["imagen"] != empresa.imagen:
                try:
                    os.remove(empresa.imagen.path)
                except Exception:
                    pass
            """
            form_empresa.save()
            form_empresa = EmpresaForm(instance=empresa)
            messages.info(request,"Cambios efectuados con éxito")
    context = {
        'form_empresa': form_empresa,
        'empresa': empresa
    }
    
    return render(request, 'empresa.html', context)



def export_pdf_view(request, id):
    id_int = int(id)
    preventivo = Preventivo.objects.get(pk=id_int)
    empresa = Empresa.objects.get(pk=1)
    productos_preventivo = ProductosPreventivo.objects.filter(preventivo=id_int)

    context = {
        'preventivo': preventivo,
        'empresa': empresa,
        'productos': productos_preventivo
    }
    html = render_to_string("pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"

    font_config = FontConfiguration()
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)

    return response


@login_required(login_url='Login')
def add_historial_preventivo_view(request):
    if request.POST:
        #print(request.POST)
        form = HistorialPreventivoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                preventivo = Preventivo.objects.get(pk=request.POST.get('preventivo'))
                preventivo.estado = 'Programado'
                date_1 = preventivo.fecha
                end_date = date_1 + timedelta(days=int(preventivo.frecuencia))
                preventivo.fecha = end_date.strftime('%Y-%m-%d')
                preventivo.save()

                #Dar de baja productos del historial
                productos_preventivo = ProductosPreventivo.objects.filter(preventivo=request.POST.get('preventivo'))
                for i in productos_preventivo:
                    obtain_product = Producto.objects.get(pk=i.producto.id)
                    suma = float(obtain_product.cantidad) - float(i.cantidad)
                    obtain_product.cantidad = suma
                    obtain_product.save()
                #Guardar Formulario

                form.save()
            except Exception as e:
                messages.warning(request, str(e))
                return redirect('Preventivos')
        else:
            messages.warning(request,'Hubo un error con el formulario')

    return redirect('Preventivos')


class materiales_preventivos(ListView):
    model = ProductosPreventivo
    template_name = 'mpreventivo.html'

    @method_decorator(login_required(login_url='Login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return ProductosPreventivo.objects.filter(
            preventivo=self.kwargs['id']
        )

    def post(self, request,*ars, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(descripcion__icontains=request.POST["term"])[0:10]:
                    item = i.toJSON()
                    item['value'] = i.descripcion
                    data.append(item)
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data,safe=False)


    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de Materiales OT preventivo # {}'.format(self.kwargs['id'])
        #context["preventivo"] = Preventivo.objects.get(pk=self.kwargs['id'])
        context["productos_lista"] = Producto.objects.all()
        context["id_preventivo"] = self.kwargs['id']
        return context

@login_required(login_url='Login')
def save_materials_view(request):
    if request.POST:
        data =[]
        try:
            action = request.POST['action']
            if action == "save":
                datos = json.loads(request.POST["verts"])
                id_preventivo = request.POST["id_preventivo"]
                productos = ProductosPreventivo.objects.filter(preventivo=id_preventivo)
                for i in productos:
                    product = Producto.objects.get(pk=i.producto.id)
                    suma = float(product.cantidad) + float(i.cantidad)
                    product.cantidad = suma
                    product.save()
                
                productos.delete()
                productos = datos["products"]
                #print(productos)
                preventivo = Preventivo.objects.get(pk=id_preventivo)
                for i in productos:
                    obtain_product = Producto.objects.get(pk=float(i["id"]))
                    suma = float(obtain_product.cantidad) - float(i["cantidad"])
                    obtain_product.cantidad = suma
                    add_product = ProductosPreventivo(preventivo=preventivo, producto=obtain_product,cantidad=float(i["cantidad"]), precio=float(i["precio"]),subtotal=float(i["subtotal"]))
                    add_product.save()
                    obtain_product.save()
                
                preventivo.subtotalpiezas = float(datos["total"])
                preventivo.save()

        except Exception as e:
            data['error'] = str(e)

    return JsonResponse(data,safe=False)


class materiales_correctivos(ListView):
    model = ProductosTrabajo
    template_name = 'mcorrectivo.html'

    @method_decorator(login_required(login_url='Login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return ProductosTrabajo.objects.filter(
            trabajo=self.kwargs['id']
        )

    def post(self, request,*ars, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(descripcion__icontains=request.POST["term"])[0:10]:
                    item = i.toJSON()
                    item['value'] = i.descripcion
                    data.append(item)
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data,safe=False)


    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de Materiales OT # {}'.format(self.kwargs['id'])
        #context["preventivo"] = Preventivo.objects.get(pk=self.kwargs['id'])
        context["productos_lista"] = Producto.objects.all()
        context["id_correctivo"] = self.kwargs['id']
        return context

@login_required(login_url='Login')
def save_materials_correctivo_view(request):
    if request.POST:
        data =[]
        try:
            action = request.POST['action']
            if action == "save":
                datos = json.loads(request.POST["verts"])
                id_correctivo = request.POST["id_correctivo"]
                productos = ProductosTrabajo.objects.filter(trabajo=id_correctivo)
                for i in productos:
                    product = Producto.objects.get(pk=i.producto.id)
                    suma = float(product.cantidad) + float(i.cantidad)
                    product.cantidad = suma
                    product.save()
                
                productos.delete()
                productos = datos["products"]
                #print(productos)
                correctivo = Trabajo.objects.get(pk=id_correctivo)
                for i in productos:
                    obtain_product = Producto.objects.get(pk=float(i["id"]))
                    suma = float(obtain_product.cantidad) - float(i["cantidad"])
                    obtain_product.cantidad = suma
                    add_product = ProductosTrabajo(trabajo=correctivo, producto=obtain_product,cantidad=float(i["cantidad"]), precio=float(i["precio"]),subtotal=float(i["subtotal"]))
                    add_product.save()
                    obtain_product.save()
                
                correctivo.subtotalpiezas = float(datos["total"])
                print(correctivo.subtotalpiezas)
                correctivo.save()

        except Exception as e:
            data['error'] = str(e)

    return JsonResponse(data,safe=False)


@login_required(login_url='Login')
def dashboard_view(request):
    if request.POST:
        data = {}
        try:
            action = request.POST['action']
            if action == 'autocomplete':
                data = []
                for i in Equipo.objects.filter(descripcion__icontains=request.POST["term"])[0:10]:
                    item = i.toJSON()
                    item['value'] = i.descripcion
                    data.append(item)
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data,safe=False)
    #currentYear = datetime.now().year
    historicos = HistorialCorrectivo.objects.all()
    context ={
        #'year': currentYear
        'historicos': historicos
    }
    return render(request, 'dashboard.html', context)



@login_required(login_url='Login')
def resultData(request):
    if request.POST:
        data ={}
        try:
            action = request.POST['action']
            if action == 'equipo':
                equipo = Equipo.objects.get(pk=request.POST["id"])

                # MTBF
                mtbf = Trabajo.objects.filter(equipo = equipo).aggregate(Avg('dif_horas'))
                data["mtbf"] = round(float(mtbf["dif_horas__avg"]),2)

                # MTTR
                mttr = HistorialCorrectivo.objects.filter(correctivo__equipo = equipo).aggregate(Avg('horas'))
                data["mttr"] = round(float(mttr["horas__avg"]),2)

                # Código para gráficas
                total_correctivos = 0
                total_preventivos = 0
                horas_preventivo = 0
                horas_correctivo = 0

                totales = []
                horas =[]
                # Historico de correctivos--------------------------------
                keys =[]
                values =[]
                
                historicos = HistorialCorrectivo.objects.filter(correctivo__equipo = equipo , fecha__gte = parse_date(request.POST["fechainicio"]), fecha__lte = parse_date(request.POST["fechafin"]))
                #historicos_json = serializers.serialize("json", historicos)
                for i in historicos:
                    total = float(i.subtotalpiezas) + float(i.subtotalmo)
                    keys.append(str(i.fecha))
                    values.append(total)
                    total_correctivos = float(total_correctivos) + float(total)
                    horas_correctivo = float(horas_correctivo) + float(i.horas)

                data["fechas"] = keys
                data["subtotales"] = values

                #Historico de preventivos-----------------------------------
                keys = []
                values = []

                historicos = HistorialPreventivo.objects.filter(preventivo__equipo = equipo , fecha__gte = parse_date(request.POST["fechainicio"]), fecha__lte = parse_date(request.POST["fechafin"]))
                #historicos_json = serializers.serialize("json", historicos)
                for i in historicos:
                    total = float(i.subtotalpiezas) + float(i.subtotalmo)
                    keys.append(str(i.fecha))
                    values.append(total)
                    total_preventivos = float(total_preventivos) + float(total)
                    horas_preventivo = float(horas_preventivo) + float(i.horas)
                
                data["fechas_p"] = keys
                data["subtotales_p"] = values

                # Enviar totales---------------------------------------------
                totales.append(total_correctivos)
                totales.append(total_preventivos)

                data["totales"] = totales
                # Horas perdidas
                horas.append(horas_correctivo)
                horas.append(horas_preventivo)

                data["horas"] = horas
                
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data,safe=False)
    
@login_required(login_url='Login')
def updateEntregados(request):
    data ={}
    if request.POST:
        try:
            datos = json.loads(request.POST["herramientas"])
            print(datos)
            action =  request.POST["action"]
            id_correctivo = request.POST["correctivo"]
            herramientas_txt = ""
            if action == 'correctivos':
                correctivo = Trabajo.objects.get(pk=int(id_correctivo))
                for i in datos: 
                    herramienta = Herramienta.objects.get(pk=int(i))
                    registro = HistorialHerramienta(herramienta=herramienta, correctivo=correctivo)
                    registro.save()
                    herramientas_txt = herramientas_txt + herramienta.descripcion + "\n"

                correctivo.herramientas = herramientas_txt
                correctivo.save()


            elif action == 'preventivos':
                preventivo = Preventivo.objects.get(pk=int(id_correctivo))
                for i in datos: 
                    herramienta = Herramienta.objects.get(pk=int(i))
                    registro = HistorialHerramienta(herramienta=herramienta, preventivo=preventivo)
                    registro.save()
                    herramientas_txt = herramientas_txt + herramienta.descripcion + "\n"
                
                preventivo.herramientas = herramientas_txt
                preventivo.save()

        except Exception as e:
            data['error'] = str(e)      
    else:
        data['error'] = "Ha ocurrido un error"
       
    
    return JsonResponse(data,safe=False)