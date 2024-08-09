from rest_framework import serializers
from django.core.exceptions import ValidationError
from apps.warehouses.models import Warehouse, Good

from .models import Shipment, Item, HistoricalShipment, HistoricalItem
from utils.serializers import BaseLogsSerizalizer, BaseModelSerializer


class ShipmentSerializer(BaseModelSerializer, serializers.ModelSerializer):
    warehouse = serializers.SlugRelatedField(
        slug_field="slug", read_only=True)

    class Meta:
        model = Shipment
        fields = ("number", "slug", "comment", "created_time",
                  "status", "warehouse",)
        read_only_fields = ("number", "slug", "created_time")


class ShipmentCreationSerializer(BaseModelSerializer, serializers.ModelSerializer):
    warehouse = serializers.SlugRelatedField(
        slug_field="slug", queryset=Warehouse.objects.all())

    class Meta:
        model = Shipment
        fields = ("number", "slug", "comment", "created_time", "warehouse")


class ItemSerializer(BaseModelSerializer, serializers.ModelSerializer):
    good = serializers.SlugRelatedField(
        slug_field="slug", read_only=True)
    task = serializers.SlugRelatedField(
        slug_field="slug", read_only=True)

    class Meta:
        model = Item
        fields = ("slug", "task", "good", "number", "created_time", "status")
        read_only_fields = ("slug", "number", "created_time")


class ItemCreationSerializer(BaseModelSerializer, serializers.ModelSerializer):
    good = serializers.SlugRelatedField(
        slug_field="slug", queryset=Good.objects.all())
    task = serializers.SlugRelatedField(
        slug_field="slug", queryset=Shipment.objects.all())

    class Meta:
        model = Item
        fields = ("slug", "task", "good", "number", "created_time", "status")


class ShipmentLogsSerializer(BaseLogsSerizalizer, serializers.ModelSerializer):

    class Meta:
        model = HistoricalShipment
        fields = "__all__"


class ItemLogsSerializer(BaseLogsSerizalizer, serializers.ModelSerializer):

    class Meta:
        model = HistoricalItem
        fields = "__all__"
