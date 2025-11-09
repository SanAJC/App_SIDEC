from django.shortcuts import render
from rest_framework import viewsets
from .models import Entidad, Denuncia
from .serializers import EntidadSerializer, DenunciaSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, action
from django_ratelimit.decorators import ratelimit
from rest_framework.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from services.views import enviar_correo_denuncia
# Create your views here.

class EntidadViewSet(viewsets.ModelViewSet):
    queryset = Entidad.objects.all()
    serializer_class = EntidadSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    #POST
    @method_decorator(ratelimit(key='user', rate='10/s', method='POST', block=True))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #GET
    @method_decorator(ratelimit(key='user', rate='10/s', method='GET', block=True))
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    #GET by id
    @method_decorator(ratelimit(key='user', rate='10/s', method='GET', block=True))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    #PUT
    @method_decorator(ratelimit(key='user', rate='10/s', method='PUT', block=True))
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #PATCH
    @method_decorator(ratelimit(key='user', rate='10/s', method='PATCH', block=True))
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #DELETE
    @method_decorator(ratelimit(key='user', rate='10/s', method='DELETE', block=True))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

class DenunciaViewSet(viewsets.ModelViewSet):
    queryset = Denuncia.objects.all()
    serializer_class = DenunciaSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()  
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:  
                return queryset 
            else:
                return queryset.filter(usuario=user) 
        else:
            return queryset.none()

    #POST
    @method_decorator(ratelimit(key='user', rate='10/s', method='POST', block=True))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            denuncia_id = serializer.instance.id
            enviar_correo_denuncia.delay(denuncia_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    #GET
    @method_decorator(ratelimit(key='user', rate='10/s', method='GET', block=True))
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    #GET by id
    @method_decorator(ratelimit(key='user', rate='10/s', method='GET', block=True))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    #PUT
    @method_decorator(ratelimit(key='user', rate='10/s', method='PUT', block=True))
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.usuario != request.user:  
            raise PermissionDenied("No tienes permiso para editar esta denuncia.")
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #PATCH
    @method_decorator(ratelimit(key='user', rate='10/s', method='PATCH', block=True))
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.usuario != request.user:  
            raise PermissionDenied("No tienes permiso para editar esta denuncia.")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #DELETE
    @method_decorator(ratelimit(key='user', rate='10/s', method='DELETE', block=True))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.usuario != request.user:  
            raise PermissionDenied("No tienes permiso para eliminar esta denuncia.")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

    
