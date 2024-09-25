import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Product, Car
from datetime import date

#Test if created products are in the product list
@pytest.mark.django_db
def test_product_view_access():
    client = Client()

    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    Product.objects.create(
        name='product1',
        days_of_growth=10,
        sale_price=100,
        cost_price=50,
        seeds_amount=5.0,
        seeding_time=40,
        watering_time=10,
    )
    Product.objects.create(
        name='product2',
        days_of_growth=12,
        sale_price=120,
        cost_price=60,
        seeds_amount=6.0,
        seeding_time=45,
        watering_time=12,
    )

    url = reverse('products')
    response = client.get(url)

    assert response.status_code == 200
    assert 'product1' in response.content.decode()
    assert 'product2' in response.content.decode()

#Test if the new product was succesfully added to the database
@pytest.mark.django_db
def test_product_add_view():
    client = Client()

    user = User.objects.create_user(username="testuser", password="testpassword")
    client.login(username='testuser', password='testpassword')

    product_data = {
        'name': 'Test Product',
        'days_of_growth': 10,
        'sale_price': 100,
        'cost_price': 50,
        'seeds_amount': 5.0,
        'seeding_time': 40,
        'watering_time': 10,

    }
    response = client.post(reverse("add-product"), data=product_data)

    if response.status_code == 200:
        form_errors = response.context['form'].errors
        print("Form Errors:", form_errors)

    assert response.status_code == 302
    product_exists = Product.objects.filter(name= product_data['name']).exists()

#Test if the product was successfully edited
@pytest.mark.django_db
def test_edit_product_view(client):
    user = User.objects.create_user(username='testuser', password='testpassword', is_superuser=True)
    client.login(username='testuser', password='testpassword')

    product = Product.objects.create(
        name='originalproduct',
        days_of_growth=10,
        sale_price=100,
        cost_price=50,
        seeds_amount=5.0,
        seeding_time=40,
        watering_time=10,
    )

    # Odeslání POST požadavku na úpravu produktu
    edit_data = {
        'name': 'updatedproduct',
        'days_of_growth': 15,
        'sale_price': 150,
        'cost_price': 60,
        'seeds_amount': 6.0,
        'seeding_time': 45,
        'watering_time': 12,
    }

    response = client.post(reverse('edit-product', kwargs={'product_pk': product.pk}), edit_data)

    assert response.status_code == 302

    product.refresh_from_db()
    assert product.name == 'updatedproduct'
    assert product.days_of_growth == 15
    assert product.sale_price == 150

#Test if the product was successfully deleted
@pytest.mark.django_db
def test_product_delete_view(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username="testuser", password="testpassword")

    product = Product.objects.create(
        name="testproduct",
        days_of_growth= 3,
        sale_price= 55,
        cost_price= 200,
        seeds_amount= 3.4,
        seeding_time= 20,
        watering_time= 10
    )

    response = client.get(reverse("delete-product", kwargs={'product_pk': product.pk}))
    assert response.status_code == 302
    assert not Product.objects.filter(pk=product.pk).exists()

#Test if the first column in the table represents today's seeding schedule
@pytest.mark.django_db
def test_seed_plan_view_today():
    user = User.objects.create_user(username='testuser', password='testpassword')

    client = Client()
    client.login(username='testuser', password='testpassword')

    response = client.get(reverse('seed-plan'))
    assert response.status_code == 200

    seed_week = response.context['seed_week']
    today = date.today().strftime("%d.%m")
    assert seed_week[0]['date'] == today

#Test if the table contains 14 columns representing 14 days
@pytest.mark.django_db
def test_seed_plan_view_length():
    client = Client()

    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    response = client.get(reverse('seed-plan'))
    assert response.status_code == 200
    seed_week = response.context['seed_week']
    assert len(seed_week) == 14
