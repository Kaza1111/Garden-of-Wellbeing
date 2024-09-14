from django.views import View
from .models import Product, Restaurant, Order, OrderItem
from django.shortcuts import render, redirect, get_object_or_404

def calculate_order_item_subtotal(order_items_to_edit):
    order_items_subtotal = []
    total = 0
    for item in order_items_to_edit:
        subtotal = item.product.sale_price * item.quantity
        order_items_subtotal.append({
            "product": item.product.name,
            "days_of_growth": item.product.days_of_growth,
            "quantity": item.quantity,
            "subtotal": subtotal,
        })
        total += subtotal

    return order_items_subtotal, total
class OrderView(View):
    def get(self, request, restaurant_pk, *args,**kwargs):
        restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)
        products = Product.objects.all()
        message = ""

        try:
            current_order = restaurant.order
            order_items = OrderItem.objects.filter(order = current_order)
            order_items_sub, total = calculate_order_item_subtotal(order_items)

        except Order.DoesNotExist:
            current_order = None
            order_items = []
            order_items_sub, total = calculate_order_item_subtotal(order_items)
            message = "No orders found"

        return render(request, "garden_app/order_detail.html", {
            "message": message,
            "restaurant":restaurant, "products": products,
            "order_items": order_items_sub,
            "total": total,
            "current_order": current_order})

    def post(self, request, restaurant_pk, *args,**kwargs):
        message = ""
        act_restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        action = request.POST.get("action")
        description = request.POST.get("description")

        if product_id and quantity:
            act_product = get_object_or_404(Product, pk = product_id)
            try:
                current_order = act_restaurant.order
                if description:
                    current_order.description = description
                    current_order.save()
                print(f"Popis try:{current_order.description}")
            except Order.DoesNotExist:
                current_order = Order.objects.create(restaurant = act_restaurant, description = description
                                if description else None )
                print(f"Popis DNE:{current_order.description}")

            act_order_item_exists = OrderItem.objects.filter(order = current_order, product = act_product).exists()

            if act_order_item_exists:
                act_order_item = OrderItem.objects.get(order = current_order, product = act_product)
                if action == "add":
                    act_order_item.quantity += int(quantity)
                if action == "subtract":
                    act_order_item.quantity -= int(quantity)
                    if act_order_item.quantity < 1:
                        act_order_item.delete()
                        act_order_item = None
            else:
                if action == "add":
                    act_order_item = OrderItem.objects.create(order = current_order, product = act_product, quantity = quantity)
                if action == "subtract":
                    act_order_item = None

            if act_order_item:
                act_order_item.save()

            products = Product.objects.all()
            order_items = OrderItem.objects.filter(order = current_order)
            order_items_sub, total = calculate_order_item_subtotal(order_items)


            return render(request, "garden_app/order_detail.html", {
                "order_items": order_items_sub,
                "message": message,
                "restaurant": act_restaurant,
                "products": products,
                "total": total,
                "current_order": current_order})

        products = Product.objects.all()
        order_items = OrderItem.objects.filter(order=act_restaurant.order) if hasattr(act_restaurant, "order") else []
        order_items_sub, total = calculate_order_item_subtotal(order_items)

        return render(request, "garden_app/order_detail.html", {
            "products": products,
            "message": message,
            "restaurant": act_restaurant,
            "order_items": order_items_sub,
            "total": total,
        })