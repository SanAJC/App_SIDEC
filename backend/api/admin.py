from django.contrib import admin
from .models import Denuncia,Entidad
# Register your models here.

class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'entidad', 'descripcion', 'estado', 'created_at', 'updated_at')
    list_filter = ('estado', 'created_at', 'updated_at')
    search_fields = ('entidad__nombre', 'descripcion')
    ordering = ('id',)

class EntidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('nombre',)
    ordering = ('id',)
