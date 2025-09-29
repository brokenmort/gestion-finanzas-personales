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
    class Meta:
        model = IngresoPago
        fields = ['id', 'ingreso_fijo', 'date', 'amount']
        read_only_fields = ['id', 'ingreso_fijo']
