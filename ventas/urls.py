from django.urls import path
from . import views

app_name = "ventas"
urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("nuevo/", views.product_create, name="product_create"),
    path("<int:pk>/", views.product_detail, name="product_detail"),
    path("<int:pk>/editar/", views.product_update, name="product_update"),
    path("<int:pk>/eliminar/", views.product_delete, name="product_delete"),
    path("ventas/", views.venta_list, name="venta_list"),
    path("ventas/nueva/", views.venta_create, name="venta_create"),
    path("ventas/<int:pk>/", views.venta_detail, name="venta_detail"),
    path("ventas/<int:pk>/eliminar/", views.venta_delete, name="venta_delete"),
    path("clientes/", views.cliente_list, name="cliente_list"),
    path("clientes/nuevo/", views.cliente_create, name="cliente_create"),
    path("clientes/<int:pk>/editar/", views.cliente_update, name="cliente_update"),
    path("clientes/<int:pk>/eliminar/", views.cliente_delete, name="cliente_delete"),
]
