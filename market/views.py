# market/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Produto, CATEGORIA_CHOICES, PLATAFORMA_CHOICES, Pedido
from .forms import ProdutoForm, CheckoutForm
from django.db import transaction

# ------------------------------
# VIEWS DO CATÁLOGO
# ------------------------------

def product_list(request):
    """View para listar produtos com busca e filtros."""
    products = Produto.objects.all().order_by('-data_cadastro')
    # Exclui itens fora de estoque
    products = products.filter(estoque__gt=0) 

    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(nome__icontains=query) | Q(descricao__icontains=query) | Q(vendedor__username__icontains=query)
        ).distinct()

    selected_category = request.GET.get('categoria')
    selected_platform = request.GET.get('plataforma')

    if selected_category:
        products = products.filter(categoria=selected_category)
    
    if selected_platform:
        products = products.filter(plataforma=selected_platform)
        
    # Adiciona lista de IDs do carrinho ao contexto para desabilitar o botão 'Adicionar ao Carrinho'
    cart_ids = request.session.get('cart', [])

    context = {
        'products': products,
        'query': query,
        'categoria_choices': CATEGORIA_CHOICES,
        'plataforma_choices': PLATAFORMA_CHOICES,
        'selected_category': selected_category,
        'selected_platform': selected_platform,
        'cart_ids': cart_ids, 
    }
    
    return render(request, 'market/product_list.html', context)

def product_detail(request, pk):
    """View para exibir os detalhes de um único produto."""
    product = get_object_or_404(Produto, pk=pk)
    
    # Adiciona informações específicas para o template
    is_in_cart = pk in request.session.get('cart', [])
    
    context = {
        'product': product,
        'is_in_cart': is_in_cart,
    }
    return render(request, 'market/product_detail.html', context)

# ------------------------------
# LÓGICA DO CARRINHO (NOVAS FUNÇÕES)
# ------------------------------

@login_required
def add_to_cart(request, pk):
    """Adiciona um produto (por PK) ao carrinho de compras na sessão."""
    cart = request.session.get('cart', [])
    if pk not in cart:
        cart.append(pk)
        request.session['cart'] = cart
        messages.success(request, 'Produto adicionado ao carrinho!')
    else:
        messages.warning(request, 'Este item já está no seu carrinho.')
        
    return redirect('market:product_detail', pk=pk) # Retorna para a página do produto

@login_required
def remove_from_cart(request, pk):
    """Remove um produto (por PK) do carrinho de compras na sessão."""
    cart = request.session.get('cart', [])
    if pk in cart:
        cart.remove(pk)
        request.session['cart'] = cart
        messages.info(request, 'Produto removido do carrinho.')
        
    return redirect('market:cart_detail')

@login_required
def cart_detail(request):
    """Exibe os produtos no carrinho do usuário."""
    cart_ids = request.session.get('cart', [])
    products = Produto.objects.filter(pk__in=cart_ids, estoque__gt=0)
    
    # Calcula o total
    total = sum(p.preco for p in products)
    
    context = {
        'products': products,
        'total': total,
    }
    return render(request, 'market/cart_detail.html', context)

@login_required
def checkout(request):
    """Processa a finalização da compra, coleta dados pessoais e simula a transação."""
    cart_ids = request.session.get('cart', [])
    products = Produto.objects.filter(pk__in=cart_ids, estoque__gt=0)
    
    if not products:
        messages.error(request, 'Seu carrinho está vazio ou os itens estão fora de estoque.')
        return redirect('market:cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            
            # BLOCO DE TRANSAÇÃO: Garante que tudo seja salvo ou nada seja salvo
            with transaction.atomic():
                # Itera sobre os produtos e finaliza a compra de cada um
                for product in products:
                    # 1. Cria o Pedido (Baseado nos dados do formulário)
                    pedido = form.save(commit=False)
                    pedido.comprador = request.user
                    pedido.vendedor_original = product.vendedor
                    pedido.produto_nome = product.nome
                    pedido.produto_preco = product.preco
                    pedido.save()
                    
                    # 2. Atualiza o Estoque (Simula a venda)
                    product.estoque -= 1
                    
                    # 3. Se o estoque zerar, o produto é removido do catálogo (lógica do usuário)
                    if product.estoque == 0:
                        messages.warning(request, f'O produto "{product.nome}" foi removido do catálogo por esgotar.')
                    
                    # Salva a alteração do estoque
                    product.save()

                # 4. Limpa o carrinho da sessão
                request.session['cart'] = []
                messages.success(request, 'Compra finalizada com sucesso! Seu pedido foi registrado.')
                
                # Redireciona para a página de sucesso com o ID do último pedido
                return redirect('market:checkout_success', pedido_id=pedido.pk)
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário de entrega.')
    else:
        # Preenche o email com o email do usuário logado, se disponível
        initial_data = {'email': request.user.email if request.user.email else ''}
        form = CheckoutForm(initial=initial_data)

    total = sum(p.preco for p in products)

    context = {
        'products': products,
        'total': total,
        'form': form,
    }
    return render(request, 'market/checkout.html', context)


def checkout_success(request, pedido_id):
    """Exibe a confirmação de compra."""
    pedido = get_object_or_404(Pedido, pk=pedido_id, comprador=request.user)
    context = {
        'pedido': pedido
    }
    return render(request, 'market/checkout_success.html', context)

# ------------------------------
# VIEWS DE AUTENTICAÇÃO E REGISTRO
# ------------------------------

def register(request):
    """View para registro de novos usuários."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('market:login')
        else:
            messages.error(request, 'Houve um erro no cadastro. Por favor, corrija os erros abaixo.')
    else:
        form = UserCreationForm()
    
    return render(request, 'market/register.html', {'form': form})

# ------------------------------
# VIEWS DO VENDEDOR (ADMIN PESSOAL)
# ------------------------------

@login_required
def create_product(request):
    """Permite ao usuário logado criar um novo anúncio."""
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES) 
        if form.is_valid():
            product = form.save(commit=False)
            product.vendedor = request.user
            product.save()
            messages.success(request, f'O anúncio "{product.nome}" foi criado com sucesso!')
            return redirect('market:user_products')
        else:
            messages.error(request, 'Ocorreu um erro ao criar o anúncio. Verifique os campos.')
    else:
        form = ProdutoForm()
        
    context = {
        'form': form,
        'title': 'Criar Novo Anúncio',
    }
    return render(request, 'market/product_form.html', context)

@login_required
def edit_product(request, pk):
    """Permite ao usuário logado editar seu próprio anúncio."""
    product = get_object_or_404(Produto, pk=pk)
    
    if product.vendedor != request.user:
        messages.error(request, 'Você não tem permissão para editar este anúncio.')
        return redirect('market:user_products')

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'O anúncio "{product.nome}" foi atualizado com sucesso!')
            return redirect('market:user_products')
        else:
            messages.error(request, 'Ocorreu um erro ao atualizar o anúncio. Verifique os campos.')
    else:
        form = ProdutoForm(instance=product)
        
    context = {
        'form': form,
        'title': f'Editar Anúncio: {product.nome}',
        'product_pk': product.pk,
    }
    return render(request, 'market/product_form.html', context)

@login_required
def delete_product(request, pk):
    """Permite ao usuário logado excluir seu próprio anúncio."""
    product = get_object_or_404(Produto, pk=pk)
    
    if product.vendedor != request.user:
        messages.error(request, 'Você não tem permissão para excluir este anúncio.')
        return redirect('market:user_products')

    if request.method == 'POST':
        product.delete()
        messages.warning(request, f'O anúncio "{product.nome}" foi excluído com sucesso.')
        return redirect('market:user_products')
        
    context = {
        'product': product,
    }
    return render(request, 'market/product_confirm_delete.html', context)

@login_required
def user_products(request):
    """Página de "administrador" pessoal onde o usuário vê seus anúncios."""
    user_listings = Produto.objects.filter(vendedor=request.user).order_by('-data_cadastro')
    
    context = {
        'products': user_listings,
    }
    return render(request, 'market/user_products.html', context)