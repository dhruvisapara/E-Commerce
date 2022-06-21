from django.apps import AppConfig



class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'category'

    def ready(self):
        super(CategoryConfig, self).ready()
        from category import signal