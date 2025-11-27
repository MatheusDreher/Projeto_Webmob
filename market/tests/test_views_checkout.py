from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from market.models import Produto

class CheckoutViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.produto = Produto.objects.create(
            vendedor=self.user,
            nome='God of War',
            descricao='IMidia Fisica',
            preco=50,
            estoque=10,
            categoria='JOGO',
            plataforma='PS5'
        )
        self.client.login(username='testuser', password='12345')

    def test_checkout_post(self):
        session = self.client.session
        session['cart'] = [self.produto.pk]
        session.save()
        data = {
            'nome_completo': 'Matheus Santos',
            'email': 'teste@example.com',
            'endereco': 'Rua A, 123',
            'cidade': 'Palmas',
            'estado': 'TO',
            'cep': '12345678'
        }
        response = self.client.post(reverse('market:checkout'), data)
        self.assertEqual(response.status_code, 302)
