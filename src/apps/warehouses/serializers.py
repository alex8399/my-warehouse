from rest_framework import serializers

from .models import Warehouse, Good, HistoricalWarehouse, HistoricalGood

from utils.serializers import BaseLogsSerizalizer, BaseModelSerializer


class WarehouseSerializer(BaseModelSerializer, serializers.ModelSerializer):

    class Meta:
        model = Warehouse
        fields = ("title", "slug", "text", "active", "created_time")
        read_only_fields = ("slug", "created_time")


class GoodSerializer(BaseModelSerializer, serializers.ModelSerializer):
    warehouse = serializers.SlugRelatedField(slug_field="slug", read_only=True)

    class Meta:
        model = Good
        fields = ("title", "slug", "warehouse", "vendor_code", "text",
                  "number", "unit", "created_time")

        read_only_fields = ("slug", "created_time", "warehouse")


class GoodFullInfoSerializer(BaseModelSerializer, serializers.ModelSerializer):
    warehouse = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    reserved_number = serializers.SerializerMethodField(
        method_name="get_reserved_number")

    def get_reserved_number(self, obj: Good) -> int:
        return obj.get_reserved_number()

    class Meta:
        model = Good
        fields = ("title", "slug", "warehouse", "vendor_code", "text",
                  "number", "reserved_number", "unit", "created_time")

        read_only_fields = ("slug", "created_time", "warehouse")


class GoodCreationSerializer(serializers.ModelSerializer):
    warehouse = serializers.SlugRelatedField(
        slug_field="slug", queryset=Warehouse.objects.all())

    class Meta:
        model = Good
        fields = ("title", "warehouse", "vendor_code", "text",
                  "number", "unit", "slug", "created_time")
        read_only_fields = ("slug", "created_time")

class WarehouseLogsSerializer(BaseLogsSerizalizer, serializers.ModelSerializer):

    class Meta:
        model = HistoricalWarehouse
        fields = "__all__"


class GoodLogsSerializer(BaseLogsSerizalizer):

    class Meta:
        model = HistoricalGood
        fields = "__all__"
