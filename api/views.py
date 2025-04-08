from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from datetime import datetime, timedelta
from .models import (
    Usuario, Gasto, Movimiento, Familia,
    CategoriaGasto, Presupuesto
)
from .serializers import (
    UsuarioSerializer, GastoSerializer, MovimientoSerializer,
    FamiliaSerializer, CategoriaGastoSerializer, PresupuestoSerializer
)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Usuario.objects.all()
        return Usuario.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def resumen(self, request):
        usuario = self.get_queryset().first()
        if not usuario:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Obtener gastos del mes actual
        hoy = datetime.now()
        inicio_mes = hoy.replace(day=1)
        gastos_mes = Gasto.objects.filter(
            usuario=usuario,
            fecha__gte=inicio_mes,
            fecha__lte=hoy
        ).aggregate(total=Sum('monto'))['total'] or 0

        # Obtener movimientos del mes actual
        movimientos_mes = Movimiento.objects.filter(
            usuario=usuario,
            fecha__gte=inicio_mes,
            fecha__lte=hoy
        ).aggregate(
            ingresos=Sum('monto', filter=Q(tipo__in=['INGRESO', 'ABONO', 'REGALO'])),
            egresos=Sum('monto', filter=Q(tipo__in=['EGRESO', 'PAGO_EFECTIVO', 'PAGO_APP']))
        )

        return Response({
            'presupuesto_mensual': usuario.presupuesto_mensual,
            'gastos_mes_actual': gastos_mes,
            'ingresos_mes_actual': movimientos_mes['ingresos'] or 0,
            'egresos_mes_actual': movimientos_mes['egresos'] or 0,
            'balance_mes_actual': (movimientos_mes['ingresos'] or 0) - (movimientos_mes['egresos'] or 0) - gastos_mes
        })


class FamiliaViewSet(viewsets.ModelViewSet):
    queryset = Familia.objects.all()
    serializer_class = FamiliaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        usuario = Usuario.objects.filter(user=self.request.user).first()
        if not usuario or not usuario.familia:
            return Familia.objects.none()
        return Familia.objects.filter(id=usuario.familia.id)


class CategoriaGastoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaGasto.objects.all()
    serializer_class = CategoriaGastoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        usuario = Usuario.objects.filter(user=self.request.user).first()
        if not usuario or not usuario.familia:
            return CategoriaGasto.objects.none()
        return CategoriaGasto.objects.filter(familia=usuario.familia)


class GastoViewSet(viewsets.ModelViewSet):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        usuario = Usuario.objects.filter(user=self.request.user).first()
        if not usuario:
            return Gasto.objects.none()
        return Gasto.objects.filter(usuario=usuario)

    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        usuario = Usuario.objects.filter(user=self.request.user).first()
        if not usuario:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        hoy = datetime.now()
        inicio_mes = hoy.replace(day=1)
        
        gastos = Gasto.objects.filter(
            usuario=usuario,
            fecha__gte=inicio_mes,
            fecha__lte=hoy
        ).values('categoria__nombre').annotate(
            total=Sum('monto')
        ).order_by('-total')

        return Response(gastos)


class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        usuario = Usuario.objects.filter(user=self.request.user).first()
        if not usuario:
            return Movimiento.objects.none()
        return Movimiento.objects.filter(usuario=usuario)

    @action(detail=False, methods=['get'])
    def resumen_mensual(self, request):
        usuario = Usuario.objects.filter(user=self.request.user).first()
        if not usuario:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        hoy = datetime.now()
        inicio_mes = hoy.replace(day=1)
        
        movimientos = Movimiento.objects.filter(
            usuario=usuario,
            fecha__gte=inicio_mes,
            fecha__lte=hoy
        ).values('tipo').annotate(
            total=Sum('monto')
        ).order_by('-total')

        return Response(movimientos)


class PresupuestoViewSet(viewsets.ModelViewSet):
    queryset = Presupuesto.objects.all()
    serializer_class = PresupuestoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        usuario = Usuario.objects.filter(user=self.request.user).first()
        if not usuario:
            return Presupuesto.objects.none()
        return Presupuesto.objects.filter(usuario=usuario)

    @action(detail=False, methods=['get'])
    def estado_actual(self, request):
        usuario = Usuario.objects.filter(user=self.request.user).first()
        if not usuario:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        hoy = datetime.now()
        inicio_mes = hoy.replace(day=1)
        
        presupuestos = Presupuesto.objects.filter(
            usuario=usuario,
            periodo_inicio__lte=hoy,
            periodo_fin__gte=hoy
        )
        
        resultado = []
        for presupuesto in presupuestos:
            gastos = Gasto.objects.filter(
                usuario=usuario,
                categoria=presupuesto.categoria,
                fecha__gte=inicio_mes,
                fecha__lte=hoy
            ).aggregate(total=Sum('monto'))['total'] or 0
            
            resultado.append({
                'categoria': presupuesto.categoria.nombre,
                'presupuesto': presupuesto.monto,
                'gastado': gastos,
                'disponible': presupuesto.monto - gastos
            })

        return Response(resultado)

def home(request):
    return HttpResponse("Bienvenido a la página principal Mario")
