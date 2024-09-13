from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user.get_full_name()}"
class Product(models.Model):
    name = models.CharField(max_length=128)
    days_of_growth = models.IntegerField()
    sale_price = models.IntegerField(default=55)
    cost_price = models.IntegerField()
    seeds_amount = models.FloatField()
    def __str__(self):
        return self.name

REGION_CHOICES = (
    ('Šumava', 'Šumava'),
    ('Českobudějovicko', 'Českobudějovicko'),
    ('Strakonicko', 'Strakonicko'),
    ('Krumlovsko', 'Krumlovsko'),
    ('Třeboňsko', 'Třeboňsko'),
    ('Lipensko', 'Lipensko')
)
class Region(models.Model):
    name = models.CharField(max_length=128, choices=REGION_CHOICES)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="regions")
    def __str__(self):
        return self.name
class Restaurant(models.Model):

    name = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    distance = models.IntegerField()
    email = models.EmailField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='restaurants')
    def __str__(self):
        return self.name

class Car(models.Model):
    type = models.CharField(max_length=128)
    year = models.IntegerField()
    consumption = models.FloatField()
    price = models.IntegerField()

    users = models.ManyToManyField(Driver, related_name='cars')

    def __str__(self):
        return self.type

class DriverCar(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.driver} - {self.car} in {self.region}"

class Order(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.restaurant.name} on {self.date}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.quantity} x {self.product} in order {self.order.restaurant}"

@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem )
def update_order_date(sender, instance, **kwargs):
    instance.order.date = timezone.now()
    instance.order.save()