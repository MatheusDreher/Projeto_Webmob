# market/models.py

from django.db import models
from django.contrib.auth.models import User

# Opções de Categoria para o Produto
CATEGORIA_CHOICES = [
    ('JOGO', 'Jogo'),
    ('CONSOLE', 'Console'),
    ('ACESSORIO', 'Acessório'),
]

# Opções de Plataforma para o Produto
PLATAFORMA_CHOICES = [
    ('PS5', 'PlayStation 5'),
    ('PS4', 'PlayStation 4'),
    ('XBOX_SERIES', 'Xbox Series S/X'),
    ('XBOX_ONE', 'Xbox One'),
    ('NINTENDO_SWITCH', 'Nintendo Switch'),
    ('PC', 'PC'),
    ('OUTRO', 'Outro'),
]

# Opções para Classificação Etária
CLASSIFICACAO_CHOICES = [
    ('L', 'Livre para todos'),
    ('+10', '+10 Anos'),
    ('+14', '+14 Anos'),
    ('+16', '+16 Anos'),
    ('+18', '+18 Anos (Adulto)'),
]

class Produto(models.Model):
    """
    Modelo para representar Jogos, Consoles e Acessórios.
    Adicionados campos de especificações técnicas.
    """
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produtos', verbose_name="Vendedor")

    nome = models.CharField(max_length=200, verbose_name="Nome do Produto")
    descricao = models.TextField(verbose_name="Descrição Detalhada")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço (R$)")
    estoque = models.IntegerField(default=0, verbose_name="Estoque Disponível")
    
    # Campo para categorizar o produto
    categoria = models.CharField(
        max_length=10,
        choices=CATEGORIA_CHOICES,
        default='JOGO',
        verbose_name="Categoria"
    )

    # Campo para indicar a plataforma
    plataforma = models.CharField(
        max_length=20,
        choices=PLATAFORMA_CHOICES,
        default='OUTRO',
        verbose_name="Plataforma"
    )

    # Campo de Imagem
    imagem = models.ImageField(
        upload_to='produtos/', 
        verbose_name="Imagem Principal do Produto",
        blank=True,
        null=True
    )
    
    data_cadastro = models.DateTimeField(auto_now_add=True)

    # ------------------------------------
    # NOVOS CAMPOS DE ESPECIFICAÇÃO
    # ------------------------------------
    # Usado para JOGOS
    genero = models.CharField(max_length=50, blank=True, null=True, verbose_name="Gênero (Jogo)")
    classificacao_etaria = models.CharField(
        max_length=5, 
        choices=CLASSIFICACAO_CHOICES, 
        default='L', 
        verbose_name="Classificação Etária", 
        blank=True, 
        null=True
    )
    
    # Usado para CONSOLES
    cpu_gpu = models.CharField(max_length=100, blank=True, null=True, verbose_name="CPU/GPU (Console)")
    memoria_ram = models.CharField(max_length=50, blank=True, null=True, verbose_name="Memória RAM (Console)")
    
    # Usado para ACESSÓRIOS
    compatibilidade = models.CharField(max_length=100, blank=True, null=True, verbose_name="Compatibilidade (Acessório)")


    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.get_categoria_display()} - Vendedor: {self.vendedor.username})"


class Pedido(models.Model):
    """
    Registra uma compra bem-sucedida.
    """
    comprador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pedidos_comprados', verbose_name="Comprador")
    vendedor_original = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pedidos_vendidos', verbose_name="Vendedor Original")
    produto_nome = models.CharField(max_length=200, verbose_name="Produto Comprado")
    produto_preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço da Compra")
    data_compra = models.DateTimeField(auto_now_add=True)
    
    # Informações de entrega
    nome_completo = models.CharField(max_length=100)
    email = models.EmailField()
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_compra']

    def __str__(self):
        return f"Pedido #{self.pk} - {self.produto_nome}"