from itertools import product
from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import AddProductForm, AddRestaurantForm
from .models import Product, Restaurant, Order, OrderItem


# Create your views here.
class ProductsListView(View):
    def get(self,request,*args,**kwargs):
        products = Product.objects.all().order_by('days_of_growth')
        return render(request, "garden_app/products.html", {'products': products})

class AddProductView(View):
    def get(self, request, *args, **kwargs):
        form = AddProductForm()
        return render(request, "garden_app/add_product.html", {'form': form})
    def post(self, request, *args, **kwargs):
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
        return render(request, "garden_app/add_product.html")

class EditProductView(View):
    def get(self, request, product_pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_pk)
        form = AddProductForm(instance=product)
        return render(request, "garden_app/edit_product.html", {'form': form})

    def post(self, request, product_pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_pk)
        form = AddProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
        return render(request, "garden_app/edit_product.html", {'form': form})

class DeleteProductView(View):
    def get(self,request,product_pk,*args,**kwargs):
        product = Product.objects.get(pk=product_pk)
        product.delete()
        return redirect('products')

class RestaurantListView(View):
    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.all().order_by('region')
        message = ""
        if not restaurants:
            message = "No Restaurants found"
        return render(request, "garden_app/restaurant_list.html", {'message':message, 'restaurants':restaurants})

class AddRestaurantView(View):
    def get(self,request,*args,**kwargs):
        form = AddRestaurantForm()
        return render(request, "garden_app/add_restaurant.html", {'form': form} )
    def post(self, request,*args,**kwargs):
        form = AddRestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant-list')
        return render(request, "garden_app/add_restaurant.html", {'form':form})

class EditRestaurantView(View):
    def get(self,request, restaurant_pk, *args,**kwargs):
        restaurant = get_object_or_404(Restaurant, pk=restaurant_pk)
        form = AddRestaurantForm(instance=restaurant)
        return render (request, "garden_app/edit_restaurant.html", {"form": form})

    def post(self, request, restaurant_pk, *args,**kwargs):
        restaurant = get_object_or_404(Restaurant, pk=restaurant_pk)
        form = AddRestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurant-list')
        return render(request, "garden_app/edit_restaurant.html", {"form": form})

class DeleteRestaurantView(View):
    def get(self, request, restaurant_pk, *args,**kwargs):
        restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)
        restaurant.delete()
        return redirect('restaurant-list')

class OrderView(View):
    def get(self, request, restaurant_pk, *args,**kwargs):
        restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)
        products = Product.objects.all()
        message = ""

        try:
            current_order = restaurant.order
            order_items = OrderItem.objects.filter(order = current_order)

        except Order.DoesNotExist:
            current_order = None
            order_items = []
            message = "No orders found"

        return render(request, "garden_app/order_detail.html", {
            "message": message,
            "restaurant":restaurant, "products": products,
            "order_items": order_items})

    def post(self, request, restaurant_pk, *args,**kwargs):
        message = ""
        act_restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        action = request.POST.get("action")

        if product_id and quantity:
            act_product = get_object_or_404(Product, pk = product_id)
            try:
                restaurant_order = act_restaurant.order
            except Order.DoesNotExist:
                restaurant_order = Order.objects.create(restaurant = act_restaurant)

            act_order_item_exists = OrderItem.objects.filter(order = restaurant_order, product = act_product).exists()

            if act_order_item_exists:
                act_order_item = OrderItem.objects.get(order = restaurant_order, product = act_product)
                if action == "add":
                    act_order_item.quantity += int(quantity)
                if action == "subtract":
                    act_order_item.quantity -= int(quantity)
            else:
                act_order_item = OrderItem.objects.create(order = restaurant_order, product = act_product,
                                                          quantity = quantity)

            act_order_item.save()

            products = Product.objects.all()
            order_items = OrderItem.objects.filter(order = restaurant_order)
            message = "Pruduct successfully added"

            return render(request, "garden_app/order_detail.html", {
                "order_items": order_items,
                "message": message,
                "restaurant": act_restaurant,
                "products": products})

        products = Product.objects.all()
        message = "Invalid product or quality"
        order_items = OrderItem.objects.filter(order = act_restaurant.order) if hasattr(act_restaurant, "order") else []

        return render(request, "garden_app/order_detail.html", {
            "products": products,
            "message": message,
            "restaurant": act_restaurant,
            "order_items": order_items
        })





