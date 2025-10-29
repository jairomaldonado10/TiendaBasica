from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    sku = models.CharField(max_length=40, unique=True)
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    def clean(self):
        if not re.fullmatch(r"[A-Z0-9\-]{3,40}", self.sku or ""):
            raise ValidationError({"sku": "Usa MAYÚSCULAS, números y guiones; 3–40 caracteres"})
    def __str__(self): return f"{self.nombre} ({self.sku})"

class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    rut = models.CharField(max_length=12, unique=True)
    email = models.EmailField(blank=True, null=True)
    def __str__(self): return f"{self.nombre} - {self.rut}"

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    total = models.PositiveIntegerField(default=0)
    def calcular_total(self): return sum(d.subtotal() for d in self.detalle_set.all())
    @transaction.atomic
    def confirmar(self):
        nuevo_total = 0
        for d in self.detalle_set.select_for_update():
            if d.cantidad <= 0: raise ValidationError("Cantidad debe ser > 0")
            if d.producto.stock < d.cantidad: raise ValidationError(f"Sin stock de {d.producto.nombre}")
            nuevo_total += d.subtotal()
        for d in self.detalle_set.select_for_update():
            p = d.producto; p.stock -= d.cantidad; p.save(update_fields=["stock"])
        self.total = nuevo_total; self.save(update_fields=["total"])
    def __str__(self): return f"Venta #{self.id or ''} - {self.cliente}"

class Detalle(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.PositiveIntegerField()
    def subtotal(self): return self.precio_unitario * self.cantidad
    def __str__(self): return f"{self.producto} x{self.cantidad}"
