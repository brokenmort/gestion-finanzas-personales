from rest_framework import serializers
from ingresos.models import IngresosFijos, IngresosExtra, IngresoPago


# ----------------------------
# SERIALIZER: IngresoPago
# ----------------------------
# Se encarga de representar los pagos individuales asociados
# a un ingreso fijo.
class IngresoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngresoPago
        # Campos expuestos al cliente
        fields = ["id", "ingreso_fijo", "date", "amount", "novelty", "novelty_amount", "novelty_reason"]
        # ingreso_fijo lo dejamos solo lectura porque
        # lo asignamos automáticamente en la vista (no lo manda el cliente)
        read_only_fields = ["id", "ingreso_fijo"]


# ----------------------------
# SERIALIZER: IngresosFijos
# ----------------------------
# Serializa ingresos fijos, incluyendo también los pagos
# asociados (relación inversa `pagos`).
class IngresosFijosSerializer(serializers.ModelSerializer):
    # El owner se muestra como el email del usuario (no editable)
    owner = serializers.ReadOnlyField(source="owner.email")
    # Relación anidada: mostramos pagos asociados a este ingreso fijo
    pagos = IngresoPagoSerializer(many=True, read_only=True)

    class Meta:
        model = IngresosFijos
        fields = ["id", "owner", "name", "reason", "quantity", "period", "pagos"]


# ----------------------------
# SERIALIZER: IngresosExtra
# ----------------------------
# Serializa ingresos extra simples (freelance, horas extra, etc.)
class IngresosExtraSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = IngresosExtra
        fields = ["id", "owner", "name", "reason", "quantity", "date"]
