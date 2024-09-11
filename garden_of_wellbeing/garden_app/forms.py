from django import forms

from .models import Product, Restaurant


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class AddRestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'