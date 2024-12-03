from django.db import models
from django.core.exceptions import ValidationError
import re


# Validación personalizada para el campo email
def validate_email_format(value):
    """
    Valida que el valor contenga un @ seguido de un . más adelante.
    """
    pattern = r'^[^@]+@[^@]+\.[^@]+$'  # Regex que asegura que exista un @ seguido de un punto
    if not re.match(pattern, value):
        raise ValidationError("El correo debe contener un '@' seguido de un '.' en un formato válido.")


class Usuario(models.Model):
    objects = None
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    estado_civil = models.CharField(max_length=50)
    fecha_estatus_civil = models.DateField()
    foto_perfil = models.ImageField(upload_to='profile_pics/')
    email = models.CharField(
        max_length=100,
        validators=[validate_email_format],  # Aplico la validación personalizada
    )

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Gasto(models.Model):
    objects = None
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='gastos')
    categoria = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.nombre} - {self.monto}"


class TipoMovimiento(models.TextChoices):
    TRANSFERENCIAS = "Transferencias"
    ABONOS = "Abonos"
    PAGOS_EFECTIVO = "Pagos de Efectivo"
    DEVOLUCIONES = "Devoluciones"
    SOBRANTES = "Sobrantes"
    PRESTAMOS_CON_INTERES = "Préstamos con Interés"
    PRESTAMOS_SIN_INTERES = "Préstamos sin Interés"
    REGALOS = "Regalos"
    ENCONTRADOS = "Encontrados"
    SIN_JUSTIFICAR = "Sin Justificar"


class Movimiento(models.Model):
    objects = None
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(
        max_length=50,
        choices=TipoMovimiento.choices,
        default=TipoMovimiento.SIN_JUSTIFICAR
    )
    descripcion = models.TextField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.monto} ({self.fecha})"
