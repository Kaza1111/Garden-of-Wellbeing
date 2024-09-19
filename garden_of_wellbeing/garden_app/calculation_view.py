from django.shortcuts import render
from django.views import View

from .models import Region, ProductCost, Product, DeliveryCost


class CalculationView(View):
    def get(self, request, *args, **kwargs):
        delivery_costs = DeliveryCost.objects.all()
        for delivery_cost in delivery_costs:
            method = delivery_cost.calculate_delivery_cost
            print(delivery_cost.total_delivery_costs)



        return render(request, 'garden_app/calculation.html', {"delivery_costs" : delivery_costs})