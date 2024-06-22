from django.apps import AppConfig

class Project4_App_levelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Project4_App_level'

    def ready(self):
        from . import signals  # Import signals here


