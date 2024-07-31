import importlib
from django.apps import AppConfig


class BookStoreAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'book_store_app'

    def ready(self):
        importlib.import_module('book_store_app.signals')
