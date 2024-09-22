from django.shortcuts import render
from django.views import View

from .models import Region, ProductCost, Product, DeliveryCost


class CalculationView(View):
    def get(self, request, *args, **kwargs):

        delivery_costs = DeliveryCost.objects.all()
        for delivery_cost in delivery_costs:
            #delivery_cost.region.calculate_delivery_time_km()
            delivery_cost.calculate_delivery_cost()
            print(delivery_cost.total_delivery_costs)

        return render(request, 'garden_app/calculation.html', {"delivery_costs" : delivery_costs})

    def post(self, request, *args, **kwargs):
        fuel_price = request.POST.get('fuel_price')
        salary = request.POST.get('salary')

        kw_price = request.POST.get('kw_price')
        watts = request.POST.get('watts')
        lighting_hours = request.POST.get('lighting_hours')

        print(salary)

        delivery_costs = DeliveryCost.objects.all()
        products = Product.objects.all()

        if kw_price or watts or lighting_hours:

            #zkusit se tam dostat přes objednávku? potřebuji přeci změnit Product costs u prodktů, které jsou v objednávce
            for product in products:
                try:
                    product_cost = ProductCost.objects.get(product=product)
                    if kw_price:
                        product_cost.kw_price = int(kw_price)

                    if watts:
                        product_cost.watts = int(watts)
                    if lighting_hours:
                        product_cost.lighting_hours = int(lighting_hours)

                    #v models změna z property na klasickou funkci
                    product_cost.save()
                    product_cost.calculate_product_cost()



                # pak lépe poladit NotExist, takto zřejmě nedostačující
                except ProductCost.DoesNotExist:
                    product_cost = None

        # funguje pouze změna u fuel cost, pořešit salary, mám definované salary ve dvou modelech, lepší mít jen v jednom?
        if fuel_price or salary or kw_price or watts or lighting_hours:
            for delivery_cost in delivery_costs:
                if fuel_price:
                    delivery_cost.fuel_price = int(fuel_price)
                if salary:
                    user = delivery_cost.car.users.first()
                    user.salary = int(salary)
                    user.save()
                #if car_consumption:
                 #   delivery_cost.car_consumption = int(car_consumption)

                # v models změna z property na klasickou funkci
                delivery_cost.calculate_delivery_cost()
                delivery_cost.save()

        return render(request, 'garden_app/calculation.html', {"delivery_costs": delivery_costs, "products": products})