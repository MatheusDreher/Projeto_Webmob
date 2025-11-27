# market/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'market'

urlpatterns = [
    # Rotas de Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='market/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('cadastro/', views.register, name='register'),
    
    # Rotas do Carrinho e Compra (NOVAS)
    path('carrinho/adicionar/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('carrinho/remover/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('carrinho/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('compra-sucesso/<int:pedido_id>/', views.checkout_success, name='checkout_success'),
    
    # Rotas do Usuário/Vendedor
    path('anunciar/', views.create_product, name='create_product'),
    path('meus-anuncios/', views.user_products, name='user_products'), 
    path('anuncio/editar/<int:pk>/', views.edit_product, name='edit_product'),
    path('anuncio/excluir/<int:pk>/', views.delete_product, name='delete_product'),
    
    # Rotas de Catálogo (Listagem e Detalhe)
    path('', views.product_list, name='product_list'),
    path('produto/<int:pk>/', views.product_detail, name='product_detail'),


    path('api/produtos/', views.api_listar_produtos, name='api_listar_produtos'),
    path('api/produtos/<int:produto_id>/', views.api_detalhe_produto, name='api_detalhe_produto'),

    path('api/meus-anuncios/', views.api_meus_produtos, name='api_meus_produtos'),
    path('api/meus-anuncios/<int:produto_id>/', views.api_meus_produtos, name='api_deletar_produto'),
    path('api/anunciar/', views.api_criar_produto, name='api_criar_produto'),

    path('api/editar-anuncio/<int:produto_id>/', views.api_editar_produto, name='api_editar_produto'),
    path('api/comprar/', views.api_realizar_compra, name='api_realizar_compra'),


]