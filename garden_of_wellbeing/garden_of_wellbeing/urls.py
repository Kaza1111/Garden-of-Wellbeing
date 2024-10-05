"""
URL configuration for garden_of_wellbeing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView

from garden_app.views import ProductsListView, AddProductView, EditProductView, DeleteProductView, RestaurantListView, \
                    AddRestaurantView, EditRestaurantView, DeleteRestaurantView, HomeView
from garden_app.class_order_view import OrderView
from garden_app.class_seed_plan_view import SeedPlanView
from garden_app.class_order_view import OrderView
from garden_app.calculation_view import CalculationView

urlpatterns = [
    #poladit redirect a homepage
    path('home/', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('products/', ProductsListView.as_view(), name='products'),
    path('add_product/', AddProductView.as_view(), name='add-product'),
    path('edit_product/<int:product_pk>/', EditProductView.as_view(), name='edit-product'),
    path('delete_product/<int:product_pk>/', DeleteProductView.as_view(), name='delete-product'),
    path('restaurant_list/', RestaurantListView.as_view(), name='restaurant-list'),
    path('add_restaurant/', AddRestaurantView.as_view(), name='add-restaurant'),
    path('edit_restaurant/<int:restaurant_pk>', EditRestaurantView.as_view(), name='edit-restaurant'),
    path('delete_restaurant/<int:restaurant_pk>', DeleteRestaurantView.as_view(), name='delete-restaurant'),
    path('order_detail/<int:restaurant_pk>', OrderView.as_view(), name='order-detail'),
    path('seed_plan_view/', SeedPlanView.as_view(), name='seed-plan'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('calculation/', CalculationView.as_view(), name='calculation')

]
