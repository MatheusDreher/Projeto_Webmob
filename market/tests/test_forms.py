from django.test import TestCase
from django.contrib.auth.models import User
from market.forms import ProdutoForm, CheckoutForm
from market.models import Produto

class ProdutoFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_form_valido(self):
        data = {
            'nome': 'God of War',
            'descricao': 'Midia Fisica',
            'preco': 50,
            'estoque': 10,
            'categoria': 'JOGO',
            'plataforma': 'PS5'
        }
        form = ProdutoForm(data)
        self.assertTrue(form.is_valid())


class CheckoutFormTest(TestCase):
    def test_form_valido(self):
        data = {
            'nome_completo': 'Matheus Santos',
            'email': 'teste@example.com',
            'endereco': 'Rua A, 123',
            'cidade': 'Palmas',
            'estado': 'TO',
            'cep': '12345678'
        }
        form = CheckoutForm(data)
        self.assertTrue(form.is_valid())
