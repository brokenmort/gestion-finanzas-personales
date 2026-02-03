from django.db import models  # Django ORM base classes and fields
from django.conf import settings  # To reference the custom user model
class IngresosFijos(models.Model):
    # Owner: user that owns this record (FK to users.User). If the user is deleted, cascade.
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ingresos_fijos')
    # Name of the income source (e.g., salary)
    name = models.CharField(max_length=255)
    # Reason or description for context
    reason = models.TextField()
    # Amount of the fixed income
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    # Period label (e.g., 'Mensual', 'Anual')
    period = models.CharField(max_length=100)
       
    class Meta:
        verbose_name_plural = "Ingresos Fijos"

    def __str__(self):
        # Human-readable representation
        return self.name

    def get_absolute_url(self):
        # Optional: path-like string for UI context
        return f"/IngresosFijos/{self.name}/"


class IngresosExtra(models.Model):
    # Owner: user that owns this record
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ingresos_extra')
    # Name of the income source (e.g., freelance)
    name = models.CharField(max_length=255)
    # Reason or description
    reason = models.TextField()
    # Amount of the extra income
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    # Effective date of the income
    date = models.DateField()
    
    class Meta:
        verbose_name_plural = "Ingresos Extra"

    def __str__(self):
        # Human-readable representation
        return self.name

    def get_absolute_url(self):
        # Optional: path-like string for UI context
        return f"/IngresosExtra/{self.name}/"
    

# Esto permitirá guardar múltiples pagos por cada ingreso fijo.
class IngresoPago(models.Model):
    ingreso_fijo = models.ForeignKey(
        'IngresosFijos',
        related_name='pagos',
        on_delete=models.CASCADE
    )
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    novelty = models.IntegerField(default=0)  # Campo adicional para novedades
    novelty_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Monto de la novedad
    novelty_reason = models.TextField(default='')  # Razón de la novedad

    class Meta:
        verbose_name_plural = "Pagos de Ingresos"

    def __str__(self):
        return f"Pago {self.amount} el {self.date} para {self.ingreso_fijo.name}"
    
