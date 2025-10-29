from django import forms
from .models import Producto, Cliente, Venta, Detalle

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "sku", "precio", "stock"]

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "rut", "email"]

class DetalleForm(forms.ModelForm):
    class Meta:
        model = Detalle
        fields = ["producto", "cantidad", "precio_unitario"]

DetalleFormSet = forms.inlineformset_factory(Venta, Detalle, form=DetalleForm, extra=1, can_delete=True)
