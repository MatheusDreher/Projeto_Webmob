from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from market.models import Produto

class PublicViewsTest(TestCase):
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

    def test_product_list_status(self):
        response = self.client.get(reverse('market:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_status(self):
        response = self.client.get(reverse('market:product_detail', args=[self.produto.pk]))
        self.assertEqual(response.status_code, 200)
