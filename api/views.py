from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from .models import Usuario, Gasto, Movimiento
from .serializers import UsuarioSerializer, GastoSerializer, MovimientoSerializer

class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class GastoViewSet(ModelViewSet):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer