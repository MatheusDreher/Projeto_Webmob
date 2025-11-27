from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from market.models import Produto

class AuthenticatedViewsTest(TestCase):
    def setUp(self):
        # Cria usuário e loga
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Cria produto com vendedor
        Produto.objects.create(
            nome='Warframe Prime',
            preco=100,
            descricao='Produto teste',
            vendedor=self.user  
        )

    def test_create_product_post(self):
        data = {
            'nome': 'God of War',
            'descricao': 'Midia Fisica',
            'preco': 50,
            'estoque': 10,
            'categoria': 'JOGO',
            'plataforma': 'PS5',
            'vendedor': self.user.id  
        }
        response = self.client.post(reverse('market:create_product'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Produto.objects.filter(nome='Warframe Prime').exists())
