from django.contrib import admin
from .models import Region, Driver, Restaurant
from django.contrib.auth.models import User
# Register your models here.

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'driver')
    search_fields = ('name',)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('user__is_staff', 'user__is_active')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Umožňuje vybrat uživatele z již existujících uživatelských účtů
        form.base_fields['user'].queryset = User.objects.all()
        return form

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'distance', 'region', 'email')
    search_fields = ('name', 'city', 'distance', 'region', 'email')
    list_filter = ('region',)