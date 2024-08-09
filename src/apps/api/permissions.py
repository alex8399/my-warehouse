from rest_framework import permissions
from apps.accounts.models import User
import utils.methods as methods

from .models import AccessAPI


class AccessAPIPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: AccessAPI) -> bool:
        permission = False
        
        if request.user.is_authenticated:
            access_API = request.user.get_access_API(warehouse=obj.warehouse)

            if access_API is not None:
                if request.method in methods.SAFE_METHODS:
                    permission = access_API.can_read_access_API(obj)
                elif request.method in methods.UPDATE_METHODS:
                    permission = access_API.can_edit_access_API(obj)
                elif request.method == methods.DELETE:
                    permission = access_API.can_delete_access_API(obj)
                elif request.method == methods.POST:
                    permission = access_API.can_create_access_API(obj)

        return permission