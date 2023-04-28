from django.contrib import admin
from index.models import Empresa
# Register your models here.
class EmpresaAdmin (admin.ModelAdmin):
    list_display = ('nombre','domicilio', 'telefono')
    search_fields = ['nombre', 'domicilio']
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Empresa, EmpresaAdmin)
