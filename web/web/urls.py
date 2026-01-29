from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# Routers de las apps
from ingresos.api.router import router_IngresosFijos, router_IngresosExtra
from egresos.api.router import router_EgresosFijos, router_EgresosExtra
from ahorros.api.router import router_ahorros
from prestamos.api.router import router_prestamos
from reports.api.views import SummaryView, CashflowMonthlyView


urlpatterns = [
    path("admin/", admin.site.urls),

    # Endpoints
    path("api/", include("users.api.router")),
    path("api/", include(router_IngresosFijos.urls)),
    path("api/", include(router_IngresosExtra.urls)),
    path("api/", include(router_EgresosFijos.urls)),
    path("api/", include(router_EgresosExtra.urls)),
    path("api/", include(router_ahorros.urls)),
    path("api/", include(router_prestamos.urls)),
    path("api/reports/summary/", SummaryView.as_view(), name="reports-summary"),
    path("api/reports/cashflow/monthly/", CashflowMonthlyView.as_view(), name="reports-cashflow-monthly"),

    # Documentación
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # raíz -> docs
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="root"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
