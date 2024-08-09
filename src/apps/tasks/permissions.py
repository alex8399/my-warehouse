from rest_framework import permissions
import utils.methods as methods
from django.shortcuts import get_object_or_404

from .models import Shipment, Item


class ShipmentPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: Shipment) -> bool:
        permission = False

        if request.user.is_authenticated:
            access_API = request.user.get_access_API(warehouse=obj.warehouse)

            if access_API is not None:
                if request.method in methods.SAFE_METHODS:
                    permission = access_API.can_read_task()
                elif request.method in methods.UPDATE_METHODS:
                    permission = access_API.can_edit_task()
                elif request.method == methods.DELETE:
                    permission = access_API.can_delete_task()
                elif request.method == methods.POST:
                    permission = access_API.can_create_task()

        return permission


class ShipmentGoodPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: Item) -> bool:
        permission = False

        if request.user.is_authenticated:
            access_API = request.user.get_access_API(warehouse=obj.task.warehouse)

            if access_API is not None:
                if request.method in methods.SAFE_METHODS:
                    permission = access_API.can_read_subtask()
                elif request.method in methods.UPDATE_METHODS:
                    permission = access_API.can_edit_subtask()
                elif request.method == methods.DELETE:
                    permission = access_API.can_delete_subtask()
                elif request.method == methods.POST:
                    permission = access_API.can_create_subtask()

        return permission


class ShipmentLogsPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        permission = False

        if request.user.is_authenticated:
            shipment = get_object_or_404(
                Shipment, slug=view.kwargs.get("slug"))
            access_API = request.user.get_access_API(
                warehouse=shipment.warehouse)

            if access_API is not None:
                permission = access_API.can_read_task_logs()

        return permission


class ShipmentGoodLogsPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        permission = False

        if request.user.is_authenticated:
            shipment_good = get_object_or_404(
                Item, slug=view.kwargs.get("slug"))
            access_API = request.user.get_access_API(
                warehouse=shipment_good.task.warehouse)

            if access_API is not None:
                permission = access_API.can_read_subtask_logs()

        return permission
