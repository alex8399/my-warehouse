from utils.paginations import StandartListPagination
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from abc import abstractmethod

from django.shortcuts import get_object_or_404

from .serializers import (ShipmentSerializer, ItemSerializer,
                          ShipmentLogsSerializer, ItemLogsSerializer,
                          ShipmentCreationSerializer, ItemCreationSerializer)
from .permissions import (ShipmentPermission, ShipmentGoodPermission,
                          ShipmentLogsPermission, ShipmentGoodLogsPermission)
from .models import Shipment, Item


class ShipmentCreateView(CreateAPIView):
    serializer_class = ShipmentCreationSerializer
    permission_classes = (ShipmentPermission,)


class ShipmentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Shipment
    serializer_class = ShipmentSerializer
    lookup_field = "slug"
    permission_classes = (ShipmentPermission,)    


class AbstractShipmentListView(ListAPIView):
    pagination_class = StandartListPagination
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        shipment = get_object_or_404(Shipment, slug=slug)
        queryset = self.get_list(shipment)
        return queryset

    @abstractmethod
    def get_list(shipment):
        pass

    def filter_queryset(self, queryset):
        return queryset.order_by("-created_time")

    class Meta:
        absctract = True


class ShipmentItemsListView(AbstractShipmentListView):
    serializer_class = ItemSerializer
    permission_classes = (ShipmentGoodPermission,)

    def get_list(self, shipment: Shipment):
        return shipment.get_items()


class ShipmentLogsListView(AbstractShipmentListView):
    serializer_class = ShipmentLogsSerializer
    permission_classes = (ShipmentLogsPermission,)

    def get_list(self, shipment):
        return shipment.get_logs()

    def filter_queryset(self, queryset):
        return queryset.order_by("-history_date")


class ItemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Item
    serializer_class = ItemSerializer
    lookup_field = "slug"
    permission_classes = (ShipmentGoodPermission,)

class ItemLogsListView(ListAPIView):
    serializer_class = ItemLogsSerializer
    pagination_class = StandartListPagination
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        shipment_good = get_object_or_404(Item, slug=slug)
        queryset = shipment_good.get_logs()
        return queryset

    def filter_queryset(self, queryset):
        return queryset.order_by("-history_date")

    class Meta:
        absctract = True


class ItemCreateView(CreateAPIView):
    serializer_class = ItemCreationSerializer
    permission_classes = (ShipmentGoodPermission,)