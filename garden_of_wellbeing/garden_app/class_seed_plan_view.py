from datetime import date, timedelta

from django.views import View
from .models import Product, Restaurant, Order, OrderItem, Region
from django.shortcuts import render, redirect, get_object_or_404
from .class_order_view import calculate_order_item_subtotal

class SeedPlanView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        orders = Order.objects.all()
        regions = Region.objects.all()
        today = date.today()

        monday_region = Region.objects.filter(delivery_day='Monday').first()
        tuesday_region = Region.objects.filter(delivery_day='Tuesday').first()
        wednesday_region = Region.objects.filter(delivery_day='Wednesday').first()
        thursday_region = Region.objects.filter(delivery_day='Thursday').first()
        friday_region = Region.objects.filter(delivery_day='Friday').first()

        for restaurant in thursday_region.restaurants.all():
            try:
                rest_order=restaurant.order
                order_items = OrderItem.objects.filter(order=rest_order)
                dict_sub, total = calculate_order_item_subtotal(order_items)
                for item in dict_sub:
                    print(item['product'])
                    print(item['quantity'])
                    print(item['days_of_growth'])
                    print("------------------------")
                #print(dict_sub[0]['days_of_growth'])
            except Order.DoesNotExist:
                rest_order = None
                print(rest_order)

        seed_week = []
        for i in range(7):
            formatted_day = today.strftime("%d.%m")
            weekday = today.strftime("%A")
            seed_week.append({weekday: formatted_day})
            today += timedelta(days=1)

        week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


        return render (request, 'garden_app/seed_plan.html', {
            'orders': orders,
            'regions': regions,
            'today': today,
            'seed_week': seed_week,
            'products': products,
            'dict_sub': dict_sub
        })