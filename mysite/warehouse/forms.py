from django import forms
from django import forms
from .models import Product, Warehouses
from django.core.exceptions import ValidationError
from .models import gen_slug


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouses
        fields = ["title", "description"]

        labels = {
            "title": "Nazwa",
            "description": "Krótki opis"
        }

        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control"})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        
        if new_slug == 'create':
            raise ValidationError('You can not make a "Create" slug! Try another name.')
        if new_slug == '':
            ps = self.cleaned_data['title'].lower()
            new_slug = gen_slug(ps)
            return new_slug
        return new_slug
    

    def clean_title(self):
        new_title = self.cleaned_data['title'].lower()

        if new_title == 'Magazyn':
            raise ValidationError('Nie możliwe jest stworzenie magazynu z nazwą "Magazyn"!')

        return new_title

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title",
            "barcode",
            "description",
            "quantity",
            "active_stamp",
            "olx_stamp",
            "price",
            "warehouse_products"
            ]
        
        labels = {
            "title": "Nazwa",
            "barcode": "Kod części",
            "description": "Krótki opis",
            "quantity": "Ilość",
            "active_stamp": "Dostępność",
            "olx_stamp": "Produdct wystawiony na OLX",
            "price": "Cena",
            "warehouse_products": 'Magazyn, na którym produkt będzie przechowywany'
        }

        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),  
            'description': forms.Textarea(attrs={"class": "form-control"}),
            'barcode': forms.TextInput(attrs={"class": "form-control"}),
            # 'quantity': forms.IntegerField(),
            # 'quantity': forms.IntegerField(),
            # 'active_stamp': forms.TextInput(attrs={'class': 'form-control'}),
            # 'olx-stamp': forms.TextInput(attrs={'class': 'form-control'}),
            # 'price': forms.TextInput(attrs={'class': 'form-control'}),
        }


    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        
        if new_slug == 'create':
            raise ValidationError('You can not make a "Create" slug! Try another name.')
        if new_slug == '':
            ps = self.cleaned_data['title'].lower()
            new_slug = gen_slug(ps)
            return new_slug
        return new_slug