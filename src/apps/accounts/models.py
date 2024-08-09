from django.contrib.auth.models import AbstractUser
from django.db import models
from typing import Sequence

from apps.api.models import AccessAPI


class User(AbstractUser):
    
    def __eq__(self, other) -> bool:
        reply = False
        if other is not None:
            reply = self.pk == getattr(other, "pk", None)
        
        return reply

    def __hash__(self) -> int:
        return hash((self.username,))

    def get_access_API(self, warehouse: 'Warehouse') -> AccessAPI | None:
        access_API_to_warehouse = None
        access_APIs = self.get_access_APIs()
        
        for access_API in access_APIs:
            if access_API.warehouse.pk == warehouse.pk:
                access_API_to_warehouse = access_API
                break

        return access_API_to_warehouse

    def has_access_API(self, warehouse: 'Warehouse') -> bool:
        return self.get_access_API(warehouse) is not None

    def get_access_APIs(self) -> Sequence[AccessAPI]:
        return self.APIs.all()
