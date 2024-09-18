from django.shortcuts import render
from django.views import View

from .models import Region, ProductCost, Product


class CalculationView(View):
    def get(self, request, *args, **kwargs):
        regions = Region.objects.all()
        products = Product.objects.all()

        for product in products:
            product_cost = ProductCost.objects.get_or_create(product = product)

        products_costs = ProductCost.objects.all()



        return render(request, 'garden_app/calculation.html', {"products_costs" : products_costs,
                                                               "regions" : regions})