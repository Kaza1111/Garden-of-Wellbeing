from django.test import TestCase

# Create your tests here.
import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

def test_product_view_access():
    client = Client()

    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    url = reverse('products')
    response = client.get(url)

    assert response.status_code == 200
    assert 'products' in response.context