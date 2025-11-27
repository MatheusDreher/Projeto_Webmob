# market/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Produto, CATEGORIA_CHOICES, PLATAFORMA_CHOICES, Pedido
from .forms import ProdutoForm, CheckoutForm
from django.db import transaction
from django.http import JsonResponse
from .models import Produto
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404

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

def api_listar_produtos(request):
    categoria = request.GET.get('categoria')
    busca = request.GET.get('busca') 
    
    produtos = Produto.objects.all()

    if categoria:
        produtos = produtos.filter(categoria=categoria)
    
    
    if busca:
        produtos = produtos.filter(Q(nome__icontains=busca) | Q(descricao__icontains=busca))

    dados = list(produtos.values('id', 'nome', 'preco', 'imagem', 'plataforma', 'categoria', 'estoque'))
    return JsonResponse(dados, safe=False)

def api_detalhe_produto(request, produto_id):
    # Filtramos pelo ID e pegamos o primeiro resultado
    produto = list(Produto.objects.filter(id=produto_id).values(
        'id', 'nome', 'descricao', 'preco', 'imagem', 
        'plataforma', 'estoque', 'categoria', 'genero'
    ))

    if produto:
        return JsonResponse(produto[0], safe=False) # Retorna só o dicionário, não uma lista
    else:
        return JsonResponse({'erro': 'Produto não encontrado'}, status=404)

@csrf_exempt # Desativa verificação de CSRF para facilitar o mobile
def api_cadastro_usuario(request):
    if request.method == 'POST':
        # Ler os dados enviados pelo Ionic
        dados = json.loads(request.body)
        username = dados.get('username')
        password = dados.get('password')
        email = dados.get('email')

        # Verifica se já existe
        if User.objects.filter(username=username).exists():
            return JsonResponse({'erro': 'Usuário já existe'}, status=400)

        # Cria o usuário
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return JsonResponse({'mensagem': 'Usuário criado com sucesso!'}, status=201)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_meus_produtos(request, produto_id=None):
    if request.method == 'GET':
        # Filtra apenas os produtos onde o 'vendedor' é o usuário do Token
        produtos = Produto.objects.filter(vendedor=request.user)
        daados = list(produtos.values('id', 'nome', 'preco', 'imagem', 'plataforma', 'estoque'))
        return Response(dados)
    
    if request.method == 'DELETE':
        
        try:
            prod = Produto.objects.get(id=produto_id, vendedor=request.user)
            prod.delete()
            return Response({'msg': 'Deletado'})
        except Produto.DoesNotExist:
            return Response({'erro': 'Produto não encontrado'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_criar_produto(request):
    # Pega os dados do formulário
    data = request.POST
    imagem = request.FILES.get('imagem') # Pega o arquivo de imagem

    estoque=data.get('estoque', 1),

    # Cria o objeto no banco
    novo_prod = Produto.objects.create(
        vendedor=request.user,
        nome=data.get('nome'),
        preco=data.get('preco'),
        descricao=data.get('descricao'),
        categoria=data.get('categoria'),
        plataforma=data.get('plataforma'),
        imagem=imagem 
    )
    return Response({'id': novo_prod.id, 'msg': 'Criado com sucesso!'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_editar_produto(request, produto_id):
    
    prod = get_object_or_404(Produto, id=produto_id, vendedor=request.user)

    
    data = request.POST
    if 'nome' in data: prod.nome = data['nome']
    if 'preco' in data: prod.preco = data['preco']
    if 'descricao' in data: prod.descricao = data['descricao']
    if 'categoria' in data: prod.categoria = data['categoria']
    if 'plataforma' in data: prod.plataforma = data['plataforma']
    if 'estoque' in data: prod.estoque = data['estoque']

    estoque=data.get('estoque', 1),

    
    nova_imagem = request.FILES.get('imagem')
    if nova_imagem:
        prod.imagem = nova_imagem

    prod.save()
    return Response({'msg': 'Produto atualizado com sucesso!'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_realizar_compra(request):
    try:
        dados = json.loads(request.body)
        ids_produtos = dados.get('ids', [])

        for id_prod in ids_produtos:
            try:
                prod = Produto.objects.get(id=id_prod)
                if prod.estoque > 0:
                    prod.estoque -= 1
                    prod.save()
            except Produto.DoesNotExist:
                pass # Se o produto não existir, ignora
        
        return Response({'msg': 'Compra realizada e estoque atualizado!'})
    except Exception as e:
        return Response({'erro': str(e)}, status=400)