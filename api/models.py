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
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    estado_civil = models.CharField(max_length=50)
    fecha_estatus_civil = models.DateField()
    foto_perfil = models.ImageField(upload_to='profile_pics/')
    email = models.CharField(
        max_length=100,
        validators=[validate_email_format],  # Se aplica la validación personalizada
    )

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Gasto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='gastos')
    categoria = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.nombre} - {self.monto}"
