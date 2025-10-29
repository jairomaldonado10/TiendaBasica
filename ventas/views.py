from types import SimpleNamespace
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from .models import Producto, Cliente, Venta
from .forms import DetalleFormSet

def product_list(request):
    q = request.GET.get("q", "")
    qs = Producto.objects.all()
    if q:
        qs = qs.filter(nombre__icontains=q)
    page = Paginator(qs.order_by("-id"), 10).get_page(request.GET.get("page"))
    return render(request, "ventas/product_list.html", {"page": page, "q": q})

def product_create(request):
    if request.method == "POST":
        nombre = (request.POST.get("nombre") or "").strip()
        sku = (request.POST.get("sku") or "").strip().upper()
        precio = int(request.POST.get("precio") or 0)
        stock = int(request.POST.get("stock") or 0)
        if not nombre or not sku or precio < 0 or stock < 0:
            messages.error(request, "Datos inválidos")
            ctx = {"form": SimpleNamespace(nombre=nombre, sku=sku, precio=precio, stock=stock)}
            return render(request, "ventas/product_form.html", ctx)
        try:
            Producto.objects.create(nombre=nombre, sku=sku, precio=precio, stock=stock)
        except IntegrityError:
            messages.error(request, "SKU duplicado")
            ctx = {"form": SimpleNamespace(nombre=nombre, sku=sku, precio=precio, stock=stock)}
            return render(request, "ventas/product_form.html", ctx)
        messages.success(request, "Producto creado")
        return redirect("ventas:product_list")
    ctx = {"form": SimpleNamespace(nombre="", sku="", precio="", stock="")}
    return render(request, "ventas/product_form.html", ctx)

def product_detail(request, pk):
    obj = get_object_or_404(Producto, pk=pk)
    return render(request, "ventas/product_detail.html", {"obj": obj})

def product_update(request, pk):
    obj = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        nombre = (request.POST.get("nombre") or "").strip()
        sku = (request.POST.get("sku") or "").strip().upper()
        precio = int(request.POST.get("precio") or 0)
        stock = int(request.POST.get("stock") or 0)
        if not nombre or not sku or precio < 0 or stock < 0:
            messages.error(request, "Datos inválidos")
            return render(request, "ventas/product_form.html", {"form": obj})
        obj.nombre = nombre
        obj.sku = sku
        obj.precio = precio
        obj.stock = stock
        try:
            obj.save()
        except IntegrityError:
            messages.error(request, "SKU duplicado")
            return render(request, "ventas/product_form.html", {"form": obj})
        messages.success(request, "Producto actualizado")
        return redirect("ventas:product_list")
    return render(request, "ventas/product_form.html", {"form": obj})

def product_delete(request, pk):
    obj = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        try:
            obj.delete()
            messages.success(request, "Producto eliminado")
        except ProtectedError:
            messages.error(request, "No se puede eliminar: el producto está usado en ventas")
        return redirect("ventas:product_list")
    return render(request, "ventas/product_delete.html", {"obj": obj})

def venta_list(request):
    page = Paginator(Venta.objects.order_by("-fecha"), 10).get_page(request.GET.get("page"))
    return render(request, "ventas/venta_list.html", {"page": page})

@transaction.atomic
def venta_create(request):
    venta = Venta()
    if request.method == "POST":
        try:
            venta.cliente_id = int(request.POST.get("cliente"))
        except (TypeError, ValueError):
            messages.error(request, "Selecciona un cliente")
            formset = DetalleFormSet(request.POST or None, instance=venta)
            return render(request, "ventas/venta_create.html", {"clientes": Cliente.objects.order_by("nombre"), "formset": formset})
        formset = DetalleFormSet(request.POST, instance=venta)
        if formset.is_valid():
            venta.save()
            formset.save()
            try:
                venta.confirmar()
            except Exception as e:
                messages.error(request, str(e))
                raise
            messages.success(request, "Venta registrada")
            return redirect("ventas:venta_list")
        messages.error(request, "Revisa los datos del detalle")
    else:
        formset = DetalleFormSet(instance=venta)
    return render(request, "ventas/venta_create.html", {"clientes": Cliente.objects.order_by("nombre"), "formset": formset})

def venta_detail(request, pk):
    obj = get_object_or_404(Venta, pk=pk)
    return render(request, "ventas/venta_detail.html", {"obj": obj})
