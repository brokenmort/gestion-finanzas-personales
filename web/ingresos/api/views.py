from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from ingresos.models import IngresosFijos, IngresosExtra, IngresoPago
from ingresos.api.serializers import (
    IngresosFijosSerializer,
    IngresosExtraSerializer,
    IngresoPagoSerializer,
)

# ============================================================
# VIEWSET: Ingresos Fijos
# ============================================================
# CRUD completo sobre IngresosFijos + un endpoint extra /pagos/
# para gestionar pagos asociados.
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["Ingresos"],
        operation_summary="Listar ingresos fijos",
        responses={200: IngresosFijosSerializer(many=True)},
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["Ingresos"],
        operation_summary="Crear ingreso fijo",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name", "reason", "quantity", "period"],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Salario"),
                "reason": openapi.Schema(type=openapi.TYPE_STRING, example="Pago mensual"),
                "quantity": openapi.Schema(type=openapi.TYPE_STRING, example="1000.00"),
                "period": openapi.Schema(type=openapi.TYPE_STRING, example="Mensual"),
            },
        ),
    ),
)
class IngresosFijosApiViewSet(ModelViewSet):
    serializer_class = IngresosFijosSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "quantity", "period"]

    def get_queryset(self):
        # Retorna solo los ingresos del usuario autenticado
        user = getattr(self.request, "user", None)
        if not user or not user.is_authenticated:
            return IngresosFijos.objects.none()
        return IngresosFijos.objects.filter(owner=user).order_by("-id")

    def perform_create(self, serializer):
        # Al crear, asignamos el usuario actual como owner
        serializer.save(owner=self.request.user)

    # ----------------------------
    # ENDPOINT EXTRA: /IngresosFijos/{id}/pagos/
    # ----------------------------
    @action(detail=True, methods=["get", "post"], url_path="pagos")
    def pagos(self, request, pk=None):
        ingreso = self.get_object()

        if request.method == "GET":
            # Listar todos los pagos de un ingreso fijo
            pagos = ingreso.pagos.all().order_by("-date")
            serializer = IngresoPagoSerializer(pagos, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            # Crear un nuevo pago asociado al ingreso fijo
            serializer = IngresoPagoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(ingreso_fijo=ingreso)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================================
# VIEWSET: Ingresos Extra
# ============================================================
# CRUD completo sobre IngresosExtra
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["Ingresos"],
        operation_summary="Listar ingresos extra",
        responses={200: IngresosExtraSerializer(many=True)},
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["Ingresos"],
        operation_summary="Crear ingreso extra",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name", "reason", "quantity", "date"],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Freelance"),
                "reason": openapi.Schema(type=openapi.TYPE_STRING, example="Proyecto web"),
                "quantity": openapi.Schema(type=openapi.TYPE_STRING, example="250.50"),
                "date": openapi.Schema(type=openapi.TYPE_STRING, example="2025-08-28"),
            },
        ),
    ),
)
class IngresosExtraApiViewSet(ModelViewSet):
    serializer_class = IngresosExtraSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "quantity", "date"]

    def get_queryset(self):
        # Retorna solo ingresos extra del usuario autenticado
        user = getattr(self.request, "user", None)
        if not user or not user.is_authenticated:
            return IngresosExtra.objects.none()
        return IngresosExtra.objects.filter(owner=user).order_by("-date", "-id")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
