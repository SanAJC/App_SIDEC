from rest_framework import serializers
from .models import Entidad, Denuncia
from authentication.models import User
from authentication.serializers import UserSerializer

class EntidadSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(use_url=True, required=False)
    class Meta:
        model = Entidad
        fields = '__all__'
    
    def get_logo(self, obj):
        if obj.logo:
            return obj.logo.url
        return None

class DenunciaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    entidad = EntidadSerializer(read_only=True)
    correo_destino = serializers.EmailField(required=False)
    pdf = serializers.FileField(required=False)
    detalle = serializers.CharField(required=False)
    entidad_id = serializers.PrimaryKeyRelatedField(
        source='entidad', 
        queryset=Entidad.objects.all(), 
        write_only=True
    )
    class Meta:
        model = Denuncia
        fields = '__all__'
    
    def create(self, validated_data):
        # Si no se proporciona correo_destino, usar el de la entidad
        if not validated_data.get('correo_destino'):
            entidad = validated_data.get('entidad')
            if entidad:
                validated_data['correo_destino'] = entidad.email
        
        return super().create(validated_data)
