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
    class Meta:
        model = Denuncia
        fields = '__all__'
