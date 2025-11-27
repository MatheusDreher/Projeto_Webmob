from django.test import SimpleTestCase
from django.urls import reverse, resolve
from market import views

class TestMarketURLs(SimpleTestCase):

    def test_product_list(self):
        url = reverse('market:product_list')
        self.assertEqual(resolve(url).func, views.product_list)

    def test_product_detail(self):
        url = reverse('market:product_detail', args=[1])
        self.assertEqual(resolve(url).func, views.product_detail)

    def test_add_to_cart(self):
        url = reverse('market:add_to_cart', args=[1])
        self.assertEqual(resolve(url).func, views.add_to_cart)

    def test_checkout(self):
        url = reverse('market:checkout')
        self.assertEqual(resolve(url).func, views.checkout)
