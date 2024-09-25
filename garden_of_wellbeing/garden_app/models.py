from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError



# Create your models here.
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=128)
    salary = models.IntegerField(default=250, validators=[MinValueValidator(50)])


    def __str__(self):
        return f"{self.user.get_full_name()}"
class Product(models.Model):
    name = models.CharField(max_length=128)
    days_of_growth = models.IntegerField(validators=[MinValueValidator(1)])
    sale_price = models.IntegerField(default=55, validators=[MinValueValidator(0)])
    cost_price = models.IntegerField(validators=[MinValueValidator(0)])
    seeds_amount = models.FloatField(validators=[MinValueValidator(0)])
    seeding_time = models.IntegerField(default=40, validators=[MinValueValidator(0)])
    watering_time = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    def __str__(self):
        return self.name

class ProductCost(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    kw_price = models.IntegerField(default=4, validators=[MinValueValidator(0)])
    watts = models.IntegerField(default=60, validators=[MinValueValidator(0)])
    lighting_hours = models.IntegerField(default=18, validators=[MinValueValidator(0), MaxValueValidator(24)])
    salary = models.PositiveIntegerField(default=250)

    total_product_cost = models.FloatField()

    #function for calculating every direct costs for products - seed cost, labor cost, light cost and sum of these values - total product cost
    def calculate_product_cost(self):
        print(self.kw_price)

        seed_cost = int((self.product.cost_price * self.product.seeds_amount / 1000))
        labor_time = int((self.product.seeding_time + (self.product.watering_time * 2 * self.product.days_of_growth)))
        labor_cost = int((labor_time * (self.salary / 3600)))
        light_cost = float(self.kw_price / 1000 * self.watts * self.lighting_hours / 48 )
        print(light_cost)
        print(f"Before:{self.total_product_cost}")
        self.total_product_cost = float(seed_cost + labor_cost + light_cost)
        print(f"After:{self.total_product_cost}")

        self.save()

        return round(self.total_product_cost,1)

REGION_CHOICES = (
    ('Šumava', 'Šumava'),
    ('Českobudějovicko', 'Českobudějovicko'),
    ('Strakonicko', 'Strakonicko'),
    ('Krumlovsko', 'Krumlovsko'),
    ('Třeboňsko', 'Třeboňsko'),
    ('Lipensko', 'Lipensko')
)
DAYS = (
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),

)
class Region(models.Model):
    #Basic atributes
    name = models.CharField(max_length=128, choices=REGION_CHOICES)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="regions")
    delivery_day = models.CharField(max_length=128, choices=DAYS)

    #Calculating atributes
    km = models.PositiveIntegerField()

    deliver_time = models.FloatField(validators=[MinValueValidator(0)])
    preparing_time = models.FloatField(validators=[MinValueValidator(0)])

    #Function for calculating total route distance (km), deliver time and preparing time for total delivering route
    #Delivery for every restaurants with order in region - one delivery route
    def calculate_delivery_time_km(self):
        kilometers = 0
        count = 0
        items_count_reg = 0
        print("vstup modelu REGION-------------------------------------------------------")
        print(f"REGION:{self.name}-----------------")
        for restaurant in self.restaurants.all():
            print(f"------RESTAURACE:{restaurant.name}")
            #kilometers += restaurant.distance
            #count += 1
            try:
                order = restaurant.order
                print(f"order existujeeeeee u :{restaurant.name}")
                items_count_rest = 0
                for item in order.items.all():
                    print(item)
                    items_count_rest += item.quantity
                if items_count_rest > 0:
                    kilometers += restaurant.distance
                    count += 1

            except Order.DoesNotExist:
                print(f"order Neexistujeeeeee u :{restaurant.name}")
                items_count_rest = 0

            print(f"Produktů v objednávce za restauraci: {items_count_rest}")
            items_count_reg += items_count_rest
            print(f"Kilometry za restiky kumulované: Přechozí porce + {restaurant.distance} = {kilometers}")
        print(f"REGION COUNT:{items_count_reg}")

        self.preparing_time = ( items_count_reg / 12 / 4 * 3 ) / 60
        print(kilometers)
        if count > 0:
            self.km = (kilometers / count * 2 * 1.5)
            print(f"Výpočet km({self.km} = {kilometers} / {count} * 2 * 1.5)")
            self.deliver_time = (self.km/ 50) + count * 0.2
        else:
            self.km = 0
            self.deliver_time = 0

        self.save()
        return self.km, self.deliver_time, self.preparing_time
    def __str__(self):
        return self.name
class Restaurant(models.Model):

    name = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    distance = models.PositiveIntegerField()
    email = models.EmailField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='restaurants')
    def __str__(self):
        return self.name

class Car(models.Model):
    car_type = models.CharField(max_length=128)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1900)])
    consumption = models.FloatField(validators=[MinValueValidator(0)])
    price = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()

    users = models.ManyToManyField(Driver, related_name='cars')

    def __str__(self):
        return self.car_type

class DeliveryCost(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="delivery_costs")
    fuel_price = models.PositiveIntegerField(default=32, validators=[MinValueValidator(0)])
    date = models.DateField(auto_now=True)


    fuel_cost = models.PositiveIntegerField(null=True, blank=True)
    salary_cost = models.PositiveIntegerField(null=True, blank=True,)

    total_products_costs = models.IntegerField(null=True, blank=True)

    total_delivery_costs = models.IntegerField(null=True, blank=True)
    total_sales = models.IntegerField(null=True, blank=True)
    margin = models.IntegerField(null=True, blank=True)

    def get_driver(self):
        return self.region.driver
    #Caluclate fuel cost, salary cost, total product costs, total delivery cost and margin for every region - delivery route
    def calculate_delivery_cost(self):
        from .class_order_view import calculate_order_item_subtotal
        print(f"++++++++++++++++++++++++REGION: {self.region} +++++++++++++++++++++++")
        
        self.fuel_cost = int(self.car.consumption / 100 * self.region.km * self.fuel_price)
        print(f"Consumption:{self.car.consumption} and Regin km:{self.region.km} and {self.fuel_price} = fuel:{self.fuel_cost}")
        #amortization
        self.region.calculate_delivery_time_km()
        self.salary_cost = int(self.car.users.first().salary * (self.region.deliver_time + self.region.preparing_time))

        print(f"Hour salary:{self.car.users.first().salary}+ Deliver region time{self.region.deliver_time}+ preparing orders time {self.region.preparing_time}= salary cost per employee:{self.salary_cost}")
        self.total_products_costs = 0
        self.total_sales = 0

        for restaurant in self.region.restaurants.all():
            print(f"{restaurant}-----------------------------")
            try:
                order = restaurant.order
                order_products_costs = 0
                items = order.items.all()
                subtotal_czk, total_czk, total_quantity = calculate_order_item_subtotal(items)
                self.total_sales += total_czk
                for item in items:
                    one_product_cost = ProductCost.objects.get(product=item.product)
                    print(f"{one_product_cost.product.name}")
                    product_costs = one_product_cost.total_product_cost * item.quantity
                    print(f"Náklady na druh jsou:{product_costs} = {item.quantity} * {one_product_cost.total_product_cost}")
                    order_products_costs += product_costs

                self.total_products_costs += int(order_products_costs)
                print(f"Order cost per restaurant: {order_products_costs}")

            except Order.DoesNotExist:
                self.total_products_costs += 0
                self.total_sales += 0
        print(f"Product cost per REGION: {self.total_products_costs}")
        print(f"TOTAL SALES:{self.total_sales}")
        self.total_delivery_costs = int(self.total_products_costs) + int(self.fuel_cost) + int(self.salary_cost)
        self.margin = int(self.total_sales - self.total_delivery_costs)
        print(f"Margin{self.margin}")
        self.save()

        print(f"Total delivery costs per {self.region.name}: {self.total_delivery_costs}")
        print("----------------------------------")
        return int(self.total_delivery_costs)

    def __str__(self):
        return f"{self.get_driver()} - {self.car} in {self.region}"

class Order(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.restaurant.name} on {self.date}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product} in order {self.order.restaurant}"

@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_date(sender, instance, **kwargs):
    instance.order.date = timezone.now()
    instance.order.save()

