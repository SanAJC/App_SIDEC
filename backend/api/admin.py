from django.contrib import admin
from .models import Denuncia,Entidad
from django.utils.html import format_html
# Register your models here.
@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'entidad', 'cuerpo', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('entidad__nombre', 'cuerpo')
    ordering = ('id',)

@admin.register(Entidad)
class EntidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'mostrar_imagen', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('nombre',)
    ordering = ('id',)

    def mostrar_imagen(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.logo.url))
        else:
            return 'No Logo'
    mostrar_imagen.short_description = 'Logo'
