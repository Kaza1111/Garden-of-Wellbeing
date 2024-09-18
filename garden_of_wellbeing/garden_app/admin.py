from django.contrib import admin
from .models import Region, Driver, Restaurant, Order, OrderItem, Car, DeliveryCost, ProductCost
from django.contrib.auth.models import User
# Register your models here.

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'driver', 'delivery_day', 'km', 'deliver_time', 'preparing_time')
    search_fields = ('name','delivery_day')

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'salary')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('user__is_staff', 'user__is_active')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Umožňuje vybrat uživatele z již existujících uživatelských účtů
        form.base_fields['user'].queryset = User.objects.all()
        return form
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_type', 'year', 'consumption', 'price', 'capacity')
    search_fields = ('car_type', 'year', 'consumption', 'users')
    list_filter = ('users',)
@admin.register(DeliveryCost)
class DeliveryCost(admin.ModelAdmin):
    list_display = ('car','region', 'driver_name', 'fuel_price', 'date', 'delivery_cost')
    search_fields = ('car', 'region', 'driver_name')
    list_filter = ('car', 'region',)

    def driver_name(self, obj):
        return obj.get_driver()  # Získá drivera z metody get_driver
        driver_name.short_description = 'Driver'
    def delivery_cost(self, obj):
        return obj.calculate_delivery_cost

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'distance', 'region', 'email')
    search_fields = ('name', 'city', 'distance', 'region', 'email')
    list_filter = ('region',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'date', 'description')
    search_fields = ('restaurant', 'date')
    list_filter = ('restaurant',)
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order', 'product', 'quantity')
    list_filter = ('product',)

@admin.register(ProductCost)
class ProductCostAdmin(admin.ModelAdmin):
    list_display = ('product', 'kw_price', 'watts', 'lighting_hours', 'salary', 'total_product_cost')

    def total_product_cost(self, obj):
        return obj.calculate_product_cost