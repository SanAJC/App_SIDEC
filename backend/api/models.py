from django.db import models
from authentication.models import User

# Create your models here.

class Entidad(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/',null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre + ' - ' + self.direccion

class Denuncia(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('error_envio', 'Error Envío'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='denuncias')
    entidad = models.ForeignKey(Entidad, on_delete=models.PROTECT, related_name='denuncias')
    asunto = models.CharField(max_length=255)
    cuerpo = models.TextField()
    email_usuario = models.EmailField()  
    detalle = models.TextField(null=True, blank=True,default='')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    pdf = models.FileField(upload_to='denuncias_pdfs/', null=True, blank=True)
    correo_destino = models.EmailField(null=True, blank=True)  # se puede rellenar automáticamente desde Entidad.correo_publico

    def __str__(self):
        return f"Denuncia {self.id} - {self.entidad.nombre} - {self.estado}"
