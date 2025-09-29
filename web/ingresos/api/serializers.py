from rest_framework import serializers
from ingresos.models import IngresosFijos, IngresosExtra, IngresoPago

class IngresosFijosSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = IngresosFijos
        fields = '__all__'  # Serializa todos los campos del modelo

class IngresosExtraSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = IngresosExtra
        fields = '__all__'  # Serializa todos los campos del modelo

class IngresoPagoSerializer(serializers.ModelSerializer):
    ingreso_fijo = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = IngresoPago
        fields = '__all__'

