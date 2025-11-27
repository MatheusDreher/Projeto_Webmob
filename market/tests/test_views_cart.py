from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from market.models import Produto

class CartViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.produto = Produto.objects.create(
            vendedor=self.user,
            nome='God of War',
            descricao='Midia Fisica',
            preco=50,
            estoque=10,
            categoria='JOGO',
            plataforma='PS5'
        )

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('market:add_to_cart', args=[self.produto.pk]))
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        self.assertIn(self.produto.pk, session.get('cart', []))

    def test_remove_from_cart(self):
        self.client.login(username='testuser', password='12345')
        session = self.client.session
        session['cart'] = [self.produto.pk]
        session.save()
        response = self.client.get(reverse('market:remove_from_cart', args=[self.produto.pk]))
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        self.assertNotIn(self.produto.pk, session.get('cart', []))
