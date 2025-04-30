from django.apps import AppConfig


class AppstartupgenezisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppStartupGenezis'

class AppStartupGeneralsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppStartupGenerals'

    def ready(self):
        import AppStartupGenezis.signals  # <- Asegurate de importar signals aquí
