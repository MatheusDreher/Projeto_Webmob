from django.apps import AppConfig


class MarketConfig(AppConfig):
    # O nome da aplicação para o Django, geralmente o nome da pasta
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market'
    verbose_name = 'Mercado de Jogos e Consoles' # Nome amigável no Admin