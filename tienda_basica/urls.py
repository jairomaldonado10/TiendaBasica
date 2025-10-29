from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("productos/", include(("ventas.urls", "ventas"), namespace="ventas")),
    path("", RedirectView.as_view(url="/productos/", permanent=False)),
]
