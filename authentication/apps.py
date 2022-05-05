from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    icon='fa fa-user'
    def ready(self):
        import authentication.signals