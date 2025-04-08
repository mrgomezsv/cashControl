from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re
from decimal import Decimal


# Validación personalizada para el campo email
def validate_email_format(value):
    """
    Valida que el valor contenga un @ seguido de un . más adelante.
    """
    pattern = r'^[^@]+@[^@]+\.[^@]+$'  # Regex que asegura que exista un @ seguido de un punto
    if not re.match(pattern, value):
        raise ValidationError("El correo debe contener un '@' seguido de un '.' en un formato válido.")


def validate_positive_amount(value):
    if value <= Decimal('0.00'):
        raise ValidationError("El monto debe ser mayor que cero.")


class Familia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    familia = models.ForeignKey(Familia, on_delete=models.SET_NULL, null=True, related_name='miembros')
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    estado_civil = models.CharField(max_length=50)
    fecha_estatus_civil = models.DateField()
    foto_perfil = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    email = models.CharField(
        max_length=100,
        validators=[validate_email_format],  # Aplico la validación personalizada
    )
    presupuesto_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class CategoriaGasto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='categorias')
    
    def __str__(self):
        return self.nombre


class Gasto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='gastos')
    categoria = models.ForeignKey(CategoriaGasto, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive_amount])
    fecha = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    comprobante = models.FileField(upload_to='comprobantes/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.monto}"


class TipoMovimiento(models.TextChoices):
    INGRESO = "Ingreso", "Ingreso"
    EGRESO = "Egreso", "Egreso"
    TRANSFERENCIA = "Transferencia", "Transferencia"
    ABONO = "Abono", "Abono"
    PAGO_EFECTIVO = "Pago Efectivo", "Pago Efectivo"
    PAGO_APP = "Pago App", "Pago App"
    DEVOLUCION = "Devolución", "Devolución"
    SOBRANTE = "Sobrante", "Sobrante"
    PRESTAMO_CON_INTERES = "Préstamo con Interés", "Préstamo con Interés"
    PRESTAMO_SIN_INTERES = "Préstamo sin Interés", "Préstamo sin Interés"
    REGALO = "Regalo", "Regalo"
    ENCONTRADO = "Encontrado", "Encontrado"
    SIN_JUSTIFICAR = "Sin Justificar", "Sin Justificar"


class Movimiento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(
        max_length=50,
        choices=TipoMovimiento.choices,
        default=TipoMovimiento.SIN_JUSTIFICAR
    )
    descripcion = models.TextField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive_amount])
    fecha = models.DateTimeField(auto_now_add=True)
    comprobante = models.FileField(upload_to='comprobantes_movimientos/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.tipo} - {self.monto} ({self.fecha})"


class Presupuesto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='presupuestos')
    categoria = models.ForeignKey(CategoriaGasto, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive_amount])
    periodo_inicio = models.DateField()
    periodo_fin = models.DateField()
    
    def __str__(self):
        return f"{self.categoria} - {self.monto} ({self.periodo_inicio} - {self.periodo_fin})"
