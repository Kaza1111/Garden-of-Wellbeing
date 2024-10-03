from django import forms

from .models import Product, Restaurant

#A form for add and edit product with all model fields
class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

#A form for add and edit restaurant with all model fields
class AddRestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'

#formu
class reviewform(forms.Form):
    number = forms.IntegerField()