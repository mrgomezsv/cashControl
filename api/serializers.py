from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Usuario, Gasto, Movimiento, Familia,
    CategoriaGasto, Presupuesto, TipoMovimiento
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class FamiliaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Familia
        fields = '__all__'


class CategoriaGastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaGasto
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Usuario
        fields = '__all__'
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        usuario = Usuario.objects.create(user=user, **validated_data)
        return usuario


class GastoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = Gasto
        fields = '__all__'


class MovimientoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Movimiento
        fields = '__all__'


class PresupuestoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = Presupuesto
        fields = '__all__'