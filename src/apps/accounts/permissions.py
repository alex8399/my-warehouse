from rest_framework import permissions

from apps.accounts.models import User

class UserPermission(permissions.BasePermission):
    
    def has_permission(self, request, view) -> bool:
        permission = False
        
        if request.user.is_authenticated and request.user.username == view.kwargs.get('username'):
            permission = True
        
        return permission