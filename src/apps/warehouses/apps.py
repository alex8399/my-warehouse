from django.apps import AppConfig
from simple_history.signals import pre_create_historical_record, post_create_historical_record


class WarehousesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.warehouses'
    verbose_name = 'Warehouses'