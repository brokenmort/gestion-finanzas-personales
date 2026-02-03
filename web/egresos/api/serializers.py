from rest_framework import serializers
from egresos.models import EgresosFijos, EgresosExtra, EgresoPago

# ----------------------------
# SERIALIZER: IngresoPago
# ----------------------------
# Se encarga de representar los pagos individuales asociados
# a un Egreso fijo.
class EgresoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EgresoPago
        # Campos expuestos al cliente
        fields = ["id", "egreso_fijo", "date", "amount", "novelty", "novelty_amount", "novelty_reason"]
        # egreso_fijo lo dejamos solo lectura porque
        # lo asignamos automáticamente en la vista (no lo manda el cliente)
        read_only_fields = ["id", "egreso_fijo"]


class EgresosFijosSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = EgresosFijos
        fields = '__all__'  # Serializa todos los campos del modelo

class EgresosExtraSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = EgresosExtra
        fields = '__all__'  # Serializa todos los campos del modelo

