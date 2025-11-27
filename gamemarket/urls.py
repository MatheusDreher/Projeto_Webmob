from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from market import views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('market.urls')), 

    # ROTAS DE AUTENTICAÇÃO
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/cadastro/', views.api_cadastro_usuario, name='api_cadastro'),
]

# Configuração de Media (Imagens)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)