from rest_framework.generics import (RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView,
                                     CreateAPIView, ListCreateAPIView)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from abc import abstractmethod


from .models import Warehouse, Good
from .serializers import (GoodSerializer, WarehouseSerializer, WarehouseLogsSerializer,
                          GoodLogsSerializer, GoodFullInfoSerializer, GoodCreationSerializer)
from .permissions import WarehousePermission, WarehouseLogsPermission, GoodPermission,  GoodLogsPermission

from apps.tasks.serializers import ShipmentSerializer
from apps.tasks.permissions import ShipmentPermission
from apps.accounts.models import User
from apps.api.serializers import AccessAPISerializer
from apps.api.models import AccessAPI
from apps.api.permissions import AccessAPIPermission

from utils.paginations import StandartListPagination


class WarehouseCreateView(CreateAPIView):
    serializer_class = WarehouseSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        warehouse = serializer.save()
        warehouse.create_access_API_for_initial_user(self.request.user)


class WarehouseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Warehouse
    serializer_class = WarehouseSerializer
    lookup_field = "slug"
    permission_classes = (WarehousePermission,)


class GoodCreateView(CreateAPIView):
    serializer_class = GoodCreationSerializer
    permission_classes = (GoodPermission,)


class GoodRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Good
    serializer_class = GoodFullInfoSerializer
    lookup_field = "slug"
    permission_classes = (GoodPermission,)

class AbstractWarehouseListView(ListAPIView):
    pagination_class = StandartListPagination
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        warehouse = get_object_or_404(Warehouse, slug=slug)
        queryset = self.get_list(warehouse)
        return queryset
    
    @abstractmethod
    def get_list(warehouse):
        pass

    def filter_queryset(self, queryset):
        return queryset.order_by("-created_time")

    class Meta:
        absctract = True


class WarehouseLogListView(AbstractWarehouseListView):
    serializer_class = WarehouseLogsSerializer
    permission_classes = (WarehouseLogsPermission,)

    def get_list(self, warehouse):
        return warehouse.get_logs()

    def filter_queryset(self, queryset):
        return queryset.order_by("-history_date")


class GoodListView(AbstractWarehouseListView):
    serializer_class = GoodSerializer
    permission_classes = (GoodPermission,)

    def get_list(self, warehouse):
        return warehouse.get_goods()


class AccessAPIListView(AbstractWarehouseListView):
    serializer_class = AccessAPISerializer
    permission_classes = (AccessAPIPermission,)

    def get_list(self, warehouse):
        return warehouse.get_access_APIs()
    
class ShipmentsListView(AbstractWarehouseListView):
    serializer_class = ShipmentSerializer
    permission_classes = (ShipmentPermission,)
    
    def get_list(self, warehouse):
        return warehouse.get_shipments()


class GoodLogListView(ListAPIView):
    serializer_class = GoodLogsSerializer
    pagination_class = StandartListPagination
    lookup_field = "slug"
    permission_classes = (GoodLogsPermission,)

    def get_list(self, warehouse):
        return warehouse.get_logs()

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        warehouse = get_object_or_404(Warehouse, slug=slug)
        queryset = self.get_list(warehouse)
        return queryset
