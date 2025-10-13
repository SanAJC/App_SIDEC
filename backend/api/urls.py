from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntidadViewSet, DenunciaViewSet

router = DefaultRouter()
router.register(r'entidades',EntidadViewSet, basename='entidad')
router.register(r'denuncias',DenunciaViewSet, basename='denuncia')

urlpatterns = [
    path('', include(router.urls)),
]