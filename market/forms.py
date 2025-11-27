# market/forms.py

from django import forms
from .models import Produto, Pedido

# Formulário para Anúncio de Produto (Criar/Editar)
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        # Inclui todos os campos de especificação
        fields = ['nome', 'descricao', 'preco', 'estoque', 'categoria', 'plataforma', 'imagem', 
                  'genero', 'classificacao_etaria', 'cpu_gpu', 'memoria_ram', 'compatibilidade']
        
        # Adiciona widgets para customizar a aparência e usar classes do Tailwind
        widgets = {
            # CAMPOS PRINCIPAIS: Largura horizontal limitada (max-w-xl), padding e arredondamento
            'nome': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary'}),
            # CORREÇÃO: Adicionado 'style': 'resize: none;'
            'descricao': forms.Textarea(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary resize-none', 'rows': 4}), 
            'preco': forms.NumberInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary'}), 
            'estoque': forms.NumberInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary'}), 
            'categoria': forms.Select(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary'}),
            'plataforma': forms.Select(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary'}),
            
            # Campos de Especificação
            'genero': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary'}),
            'classificacao_etaria': forms.Select(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary'}),
            'cpu_gpu': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary'}),
            'memoria_ram': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary'}),
            'compatibilidade': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary'}),
        }


# Formulário para Checkout (Informações do Comprador)
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nome_completo', 'email', 'endereco', 'cidade', 'estado', 'cep']
        
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-secondary focus:border-secondary'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-secondary focus:border-secondary'}),
            'endereco': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-secondary focus:border-secondary'}),
            'cidade': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-secondary focus:border-secondary'}),
            'estado': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-secondary focus:border-secondary'}),
            'cep': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-secondary focus:border-secondary'}),
        }