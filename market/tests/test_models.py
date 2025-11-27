from django.test import TestCase
from django.contrib.auth.models import User
from market.models import Produto, Pedido

class ProdutoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_criacao_produto(self):
        produto = Produto.objects.create(
            vendedor=self.user,
            nome='Warframe Prime',
            descricao='Item raro',
            preco=50,
            estoque=10,
            categoria='JOGO',
            plataforma='PS5'
        )
        self.assertEqual(str(produto), f"Warframe Prime ({produto.get_categoria_display()} - Vendedor: {self.user.username})")
        self.assertEqual(produto.estoque, 10)
        self.assertEqual(produto.preco, 50)


class PedidoModelTest(TestCase):
    def setUp(self):
        self.user_comprador = User.objects.create_user(username='comprador', password='12345')
        self.user_vendedor = User.objects.create_user(username='vendedor', password='12345')
        self.produto = Produto.objects.create(
            vendedor=self.user_vendedor,
            nome='God of War',
            descricao='IMidia Fisica',
            preco=50,
            estoque=10,
            categoria='JOGO',
            plataforma='PS5'
        )

    def test_criacao_pedido(self):
        pedido = Pedido.objects.create(
            comprador=self.user_comprador,
            vendedor_original=self.produto.vendedor,
            produto_nome=self.produto.nome,
            produto_preco=self.produto.preco,
            nome_completo='Matheus Santos',
            email='teste@example.com',
            endereco='Rua A, 123',
            cidade='Palmas',
            estado='TO',
            cep='12345678'
        )
        self.assertEqual(str(pedido), f"Pedido #{pedido.pk} - {self.produto.nome}")
        self.assertEqual(pedido.produto_preco, 50)
