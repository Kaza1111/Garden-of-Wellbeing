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
    salary = models.IntegerField(default=250)


    def __str__(self):
        return f"{self.user.get_full_name()}"
class Product(models.Model):
    name = models.CharField(max_length=128)
    days_of_growth = models.IntegerField()
    sale_price = models.IntegerField(default=55)
    cost_price = models.IntegerField()
    seeds_amount = models.FloatField()
    seeding_time = models.IntegerField(default=40)
    watering_time = models.IntegerField(default=10)
    def __str__(self):
        return self.name

class ProductCost(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    kw_price = models.IntegerField(default=4)
    watts = models.IntegerField(default=60)
    lighting_hours = models.IntegerField(default=18)
    salary = models.IntegerField(default=250)
    total_product_cost = models.IntegerField()

    #možná je blbost mít tuto funkci v modelu
    #@property
    def calculate_product_cost(self):
        seed_cost = int((self.product.cost_price * self.product.seeds_amount / 1000))
        labor_time = int((self.product.seeding_time + (self.product.watering_time * 2 * self.product.days_of_growth)))
        labor_cost = int((labor_time * (self.salary / 3600)))
        light_cost = int((self.kw_price / 1000 * self.watts * self.lighting_hours / 48 ))
        self.total_product_cost = int(seed_cost + labor_cost + light_cost)

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
    name = models.CharField(max_length=128, choices=REGION_CHOICES)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="regions")
    delivery_day = models.CharField(max_length=128, choices=DAYS)
    km = models.IntegerField()
    deliver_time = models.FloatField()
    preparing_time = models.FloatField()

    def calculate_delivery_time_km(self):
        kilometers = 0
        count = 0
        deliver_hours = 0
        items_count_reg = 0
        print(self.name)
        for restaurant in self.restaurants.all():
            print(restaurant)
            kilometers += restaurant.distance
            count += 1
            deliver_hours += kilometers / 50
            try:
                order = restaurant.order
                items_count_rest = 0
                for item in order.items.all():
                    items_count_rest += 1
                    print(items_count_rest)
            except Order.DoesNotExist:
                items_count_rest = 0

            items_count_reg += items_count_rest
        print(f"REGION COUNT:{items_count_reg}")

        self.preparing_time = items_count_reg / 12 / 4 * 3
        self.deliver_time = deliver_hours + count * 0.2
        self.km = (kilometers / count * 2 * 1.5)
        self.save()
        return self.km, self.deliver_time, self.preparing_time
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
    car_type = models.CharField(max_length=128)
    year = models.IntegerField()
    consumption = models.FloatField()
    price = models.IntegerField()
    capacity = models.IntegerField()

    users = models.ManyToManyField(Driver, related_name='cars')

    def __str__(self):
        return self.car_type

class DeliveryCost(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="delivery_costs")
    fuel_price = models.IntegerField(default=32)
    date = models.DateField(auto_now=True)

    fuel_cost = models.IntegerField(null=True, blank=True)
    salary_cost = models.IntegerField(null=True, blank=True,)
    total_products_costs = models.IntegerField(null=True, blank=True)
    total_delivery_costs = models.IntegerField(null=True, blank=True)
    total_sales = models.IntegerField(null=True, blank=True)
    margin = models.IntegerField(null=True, blank=True)

    def get_driver(self):
        return self.region.driver

    #možná blbost mít tuto funkci v modelu
    #@property
    def calculate_delivery_cost(self):
        from .class_order_view import calculate_order_item_subtotal
        print(f"++++++++++++++++++++++++REGION: {self.region} +++++++++++++++++++++++")
        
        self.fuel_cost = int(self.car.consumption / 100 * self.region.km * self.fuel_price)
        print(f"fuel:{self.fuel_cost}")
        #amortization
        self.salary_cost = int(self.car.users.first().salary * (self.region.deliver_time + self.region.preparing_time))
        print(f"salary:{self.salary_cost}")
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
                    product_costs = one_product_cost.calculate_product_cost() * item.quantity
                    print(f"{item.product}:{product_costs}")
                    order_products_costs += product_costs

                self.total_products_costs += int(order_products_costs)
                print(f"Order cost per restaurant: {order_products_costs}")

            except Order.DoesNotExist:
                self.total_products_costs += 0
                self.total_sales += 0
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
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.quantity} x {self.product} in order {self.order.restaurant}"

@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_date(sender, instance, **kwargs):
    instance.order.date = timezone.now()
    instance.order.save()

#@receiver(post_save, sender=Order)
#def update_order_date_desc(sender, instance, **kwargs):
 #   instance.date = timezone.now()
  #  instance.save()
