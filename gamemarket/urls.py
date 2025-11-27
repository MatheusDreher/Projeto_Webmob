# gamemarket/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importação para acessar as configurações
from django.conf.urls.static import static # Importação para servir arquivos

urlpatterns = [
    # URL para o painel de administração
    path('admin/', admin.site.urls),
    
    # Inclui todas as URLs da aplicação 'market' na raiz do site ('/')
    path('', include('market.urls')),
]

# NOVO: Adiciona a rota para servir arquivos de mídia APENAS em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)