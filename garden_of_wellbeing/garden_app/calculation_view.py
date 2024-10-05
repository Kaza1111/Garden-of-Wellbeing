from django.shortcuts import render
from django.views import View

from .models import Region, ProductCost, Product, DeliveryCost


#Display the table with basic overview for every region (Sales, Delivery costs, Product costs, Margin,...)
class CalculationView(View):
    def get(self, request, *args, **kwargs):

        delivery_costs = DeliveryCost.objects.all()
        for delivery_cost in delivery_costs:
            delivery_cost.calculate_delivery_cost()
            print(delivery_cost.total_delivery_costs)

        return render(request, 'garden_app/calculation.html', {"delivery_costs" : delivery_costs})

#Posibility to change some parameters, the change will edit the table
    def post(self, request, *args, **kwargs):
        fuel_price = request.POST.get('fuel_price')
        salary = request.POST.get('salary')

        kw_price = request.POST.get('kw_price')
        watts = request.POST.get('watts')
        lighting_hours = request.POST.get('lighting_hours')

        errors = {}

        #  Validation of positive number
        if fuel_price and int(fuel_price) < 0:
            errors['fuel_price'] = "ERROR: Number must be greater than 0"
        if salary and int(salary) < 0:
            errors['salary'] = "ERROR: Number must be greater than 0"
        if kw_price and int(kw_price) < 0:
            errors['kw_price'] = "ERROR: Number must be greater than 0"
        if watts and int(watts) < 0:
            errors['watts'] = "ERROR: Number must be greater than 0"
        if lighting_hours and int(lighting_hours) < 0:
            errors['lighting_hours'] = "ERROR: Number must be greater than 0"

        # If error, display message
        if errors:
            return render(request, 'garden_app/calculation.html', {
                'errors': errors,
                'fuel_price': fuel_price,
                'salary': salary,
                'kw_price': kw_price,
                'watts': watts,
                'lighting_hours': lighting_hours,
            })

        print(salary)

        delivery_costs = DeliveryCost.objects.all()
        products = Product.objects.all()

        if kw_price or watts or lighting_hours:
            for product in products:
                try:
                    product_cost = ProductCost.objects.get(product=product)
                    if kw_price:
                        product_cost.kw_price = int(kw_price)
                    if watts:
                        product_cost.watts = int(watts)
                    if lighting_hours:
                        product_cost.lighting_hours = int(lighting_hours)

                    product_cost.save()
                    product_cost.calculate_product_cost()

                except ProductCost.DoesNotExist:
                    product_cost = None

        if fuel_price or salary or kw_price or watts or lighting_hours:
            for delivery_cost in delivery_costs:
                if fuel_price:
                    delivery_cost.fuel_price = int(fuel_price)
                if salary:
                    user = delivery_cost.car.users.first()
                    user.salary = int(salary)
                    user.save()

                delivery_cost.calculate_delivery_cost()
                delivery_cost.save()

        return render(request, 'garden_app/calculation.html', {"delivery_costs": delivery_costs, "products": products})