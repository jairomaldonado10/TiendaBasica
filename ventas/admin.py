from django.contrib import admin
from django.db.models import Sum
from .models import Producto, Cliente, Venta, Detalle

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre","sku","precio","stock")
    search_fields = ("nombre","sku")
    list_editable = ("precio","stock")
    list_per_page = 20

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre","rut","email")
    search_fields = ("nombre","rut","email")
    list_per_page = 20

class DetalleInline(admin.TabularInline):
    model = Detalle
    extra = 1

@admin.action(description="Recalcular total")
def recalcular_total(modeladmin, request, qs):
    for v in qs:
        v.total = v.calcular_total()
        v.save(update_fields=["total"])

@admin.action(description="Reporte monto seleccionado")
def reporte_monto(modeladmin, request, qs):
    total = qs.aggregate(m=Sum("total"))["m"] or 0
    modeladmin.message_user(request, f"Monto: ${total:,}")

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id","cliente","fecha","total")
    date_hierarchy = "fecha"
    list_filter = ("fecha","cliente")
    search_fields = ("cliente__nombre","cliente__rut")
    inlines = [DetalleInline]
    actions = [recalcular_total, reporte_monto]
    list_per_page = 20
