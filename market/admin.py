# market/admin.py

from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Campos exibidos na lista de produtos no admin
    list_display = ('nome', 'categoria', 'plataforma', 'preco', 'estoque', 'vendedor', 'data_cadastro')
    # Filtros laterais para facilitar a busca
    list_filter = ('categoria', 'plataforma', 'estoque')
    # Campos que podem ser pesquisados
    search_fields = ('nome', 'descricao')
    # Campos que aparecem nos detalhes do produto
    fieldsets = (
        (None, {
            # CORREÇÃO: 'imagem_url' foi substituído por 'imagem'
            'fields': ('vendedor', 'nome', 'descricao', 'preco', 'estoque', 'imagem')
        }),
        ('Classificação', {
            'fields': ('categoria', 'plataforma'),
            'description': 'Define se é um jogo, console ou acessório e sua plataforma.',
        }),
        ('Especificações de Jogo', {
            'fields': ('genero', 'classificacao_etaria'),
            'description': 'Preencher apenas para Categoria: JOGO.',
        }),
        ('Especificações de Console', {
            'fields': ('cpu_gpu', 'memoria_ram'),
            'description': 'Preencher apenas para Categoria: CONSOLE.',
        }),
        ('Especificações de Acessório', {
            'fields': ('compatibilidade',),
            'description': 'Preencher apenas para Categoria: ACESSÓRIO.',
        }),
    )