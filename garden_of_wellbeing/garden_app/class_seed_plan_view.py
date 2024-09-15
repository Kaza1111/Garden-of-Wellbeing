from datetime import date, timedelta
from django.views import View
from .models import Product, Restaurant, Order, OrderItem, Region
from django.shortcuts import render
from .class_order_view import calculate_order_item_subtotal


class SeedPlanView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        orders = Order.objects.all()
        regions = Region.objects.all()
        today = date.today()

        # Barvy pro každý den v týdnu
        weekday_colors = {
            'Monday': '#FFD700',  # žlutá
            'Tuesday': '#FFA500',  # oranžová
            'Wednesday': '#FF6347',  # červená
            'Thursday': '#ADFF2F',  # zelená
            'Friday': '#FFC0CB',  # růžová
            'Saturday': '#87CEEB',  # modrá
            'Sunday': '#9370DB'  # fialová
        }

        # Definování týdenních dnů pro výpočet doručení
        week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Vytvoření seed_week se 14 dny
        seed_week = []
        current_day = today
        for i in range(14):  # Rozšíření na 14 dnů
            weekday = current_day.strftime("%A")
            seed_week.append({
                'weekday': weekday,
                'date': current_day.strftime("%d.%m"),
                'color': weekday_colors[weekday]
            })
            current_day += timedelta(days=1)

        # Vytvoření prázdného slovníku pro počty produktů podle dní a barev
        product_counts = {}
        for product in products:
            product_counts[product.pk] = {}

        # Projít regiony a restaurace, zjistit den doručení a počty produktů
        for region in regions:
            delivery_weekday = region.delivery_day  # Přímo použijeme den doručení jako řetězec

            for restaurant in region.restaurants.all():
                try:
                    rest_order = restaurant.order
                    order_items = OrderItem.objects.filter(order=rest_order)

                    dict_sub, total, total_quantity = calculate_order_item_subtotal(order_items)
                    total_quantity_growth_day = 0

                    for item in dict_sub:
                        product = item['product']
                        quantity = item['quantity']
                        growth_days = item['days_of_growth']

                        # Kdy má být produkt zaset
                        delivery_day = today + timedelta((week.index(delivery_weekday) - today.weekday()) % 7)
                        seed_day = delivery_day - timedelta(days=growth_days)
                        seed_weekday = seed_day.strftime('%A')

                        # Přidej počty a barvy do slovníku product_counts
                        if product.pk not in product_counts:
                            product_counts[product.pk] = {}

                        if seed_weekday not in product_counts[product.pk]:
                            product_counts[product.pk][seed_weekday] = {
                                'count': 0,
                                'delivery_color': weekday_colors[delivery_weekday]
                            }

                        product_counts[product.pk][seed_weekday]['count'] += quantity
                        total_quantity_growth_day += product_counts[product.pk][seed_weekday]['count']

                except Order.DoesNotExist:
                    continue

        # Předat data do šablony
        return render(request, 'garden_app/seed_plan.html', {
            'products': products,
            'seed_week': seed_week,
            'product_counts': product_counts,
            'total_quantity_growth_day': total_quantity_growth_day
        })










