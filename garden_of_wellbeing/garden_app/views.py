from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .class_order_view import calculate_order_item_subtotal
from .forms import AddProductForm, AddRestaurantForm
from .models import Product, Restaurant, Order, OrderItem


# Create your views here.
# Get list of products, with buttons "edit","add" and "delete"

# Dedil bych z této třídy, místo LoginRequired


class LoggedInView(LoginRequiredMixin, View):
    login_url = '/login/'


class ProductsListView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all().order_by('days_of_growth')
        return render(request, "garden_app/products.html", {'products': products})


# Possibility to add a new product, display a form
class AddProductView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, *args, **kwargs):
        form = AddProductForm()
        return render(request, "garden_app/add_product.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
        return render(request, "garden_app/add_product.html", {"form": form})


# Posibility to edit existing product, display a form
class EditProductView(PermissionRequiredMixin, View):
    permission_required = 'garden_app.change_product'

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


# Posibility to delete existing product if you click the button
class DeleteProductView(PermissionRequiredMixin,View):
    permission_required = 'garden_app.delete_product'

    def get(self, request, product_pk, *args, **kwargs):
        product = Product.objects.get(pk=product_pk)
        product.delete()
        return redirect('products')


# Display a list of restaurants with total sales and quantites, if not any restaurant, display message
class RestaurantListView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.all().order_by('region')
        restaurants_data = []
        total_together = 0
        total_together_quantity = 0

        for restaurant in restaurants:
            try:
                restaurant_order = Order.objects.get(restaurant=restaurant)
                order_items = OrderItem.objects.filter(order=restaurant_order)
                order_items_sub, total, total_quantity = calculate_order_item_subtotal(order_items)

            except Order.DoesNotExist:
                restaurant_order = None
                order_items = []
                total = 0
                total_quantity = 0

            restaurants_data.append({
                'restaurant': restaurant,
                'order_items': order_items,
                'total': total,
                'total_quantity': total_quantity,
            })
            total_together += total
            total_together_quantity += total_quantity
        message = ""
        if not restaurants:
            message = "No Restaurants found"

        return render(request, "garden_app/restaurant_list.html", {
            'message': message, 'restaurants_data': restaurants_data, 'total_together': total_together,
            'total_together_quantity': total_together_quantity
        })


# Posibility to add a new restaurant, display a form
class AddRestaurantView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, *args, **kwargs):
        form = AddRestaurantForm()
        return render(request, "garden_app/add_restaurant.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddRestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant-list')
        return render(request, "garden_app/add_restaurant.html", {'form': form})


# Posibility to edit existing restaurant, display a form
class EditRestaurantView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, restaurant_pk, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=restaurant_pk)
        form = AddRestaurantForm(instance=restaurant)
        return render(request, "garden_app/edit_restaurant.html", {"form": form})

    def post(self, request, restaurant_pk, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=restaurant_pk)
        form = AddRestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurant-list')
        return render(request, "garden_app/edit_restaurant.html", {"form": form})


# Posibility to delete existing restaurant
class DeleteRestaurantView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, restaurant_pk, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=restaurant_pk)
        restaurant.delete()
        return redirect('restaurant-list')

class HomeView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args, **kwargs):
        return render(request, "garden_app/home.html")
