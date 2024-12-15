from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from .models import Usuario, Gasto, Movimiento
from .serializers import UsuarioSerializer, GastoSerializer, MovimientoSerializer

class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class GastoViewSet(ModelViewSet):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer

class MovimientoViewSet(ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer

def home(request):
    return HttpResponse("Bienvenido a la página principal")
