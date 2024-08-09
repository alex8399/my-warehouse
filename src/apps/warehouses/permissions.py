from rest_framework import permissions
from apps.accounts.models import User
import utils.methods as methods

from django.shortcuts import get_object_or_404

from .models import Warehouse, Good


class WarehousePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: Warehouse) -> bool:
        permission = False

        if request.user.is_authenticated:
            access_API = request.user.get_access_API(warehouse=obj)

            if access_API is not None:
                if request.method in methods.SAFE_METHODS:
                    permission = access_API.can_read_warehouse()
                elif request.method in methods.UPDATE_METHODS:
                    permission = access_API.can_edit_warehouse()
                elif request.method == methods.DELETE:
                    permission = access_API.can_delete_warehouse()

        return permission


class WarehouseLogsPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        permission = False

        if request.user.is_authenticated:
            warehouse = get_object_or_404(
                Warehouse, slug=view.kwargs.get("slug"))
            access_API = request.user.get_access_API(warehouse=warehouse)

            if access_API is not None:
                permission = access_API.can_read_warehouse_logs()

        return permission


class GoodPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: Good) -> bool:
        permission = False

        if request.user.is_authenticated:
            access_API = request.user.get_access_API(warehouse=obj.warehouse)

            if access_API is not None:
                if request.method in methods.SAFE_METHODS:
                    permission = access_API.can_read_good()
                elif request.method in methods.UPDATE_METHODS:
                    permission = access_API.can_edit_good()
                elif request.method == methods.DELETE:
                    permission = access_API.can_delete_good()
                elif request.method == methods.POST:
                    permission = access_API.can_create_good()

        return permission


class GoodLogsPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        permission = False

        if request.user.is_authenticated:
            good = get_object_or_404(Good, slug=view.kwargs.get("slug"))
            access_API = request.user.get_access_API(warehouse=good.warehouse)

            if access_API is not None:
                permission = access_API.can_read_good_logs()

        return permission
