from rest_framework import serializers

from .models import AccessAPI
from apps.warehouses.models import Warehouse
from apps.accounts.models import User

from utils.serializers import BaseModelSerializer


class AccessAPISerializer(BaseModelSerializer, serializers.ModelSerializer):
    user = serializers.SerializerMethodField(
        method_name="get_user")
    user_first_name = serializers.SerializerMethodField(
        method_name="get_user_first_name")
    user_last_name = serializers.SerializerMethodField(
        method_name="get_user_last_name")
    user_email = serializers.SerializerMethodField(
        method_name="get_user_email")
    user_active = serializers.SerializerMethodField(
        method_name="get_user_active")
    
    warehouse = serializers.SerializerMethodField(
        method_name="get_warehouse")
    warehouse_title = serializers.SerializerMethodField(
        method_name="get_warehouse_title")
    warehouse_active = serializers.SerializerMethodField(
        method_name="get_warehouse_active")
    
    def get_user(self, obj: AccessAPI) -> str:
        return obj.user.username
    
    def get_user_first_name(self, obj: AccessAPI) -> str:
        return obj.user.first_name

    def get_user_last_name(self, obj: AccessAPI) -> str:
        return obj.user.last_name

    def get_user_email(self, obj: AccessAPI) -> str:
        return obj.user.email

    def get_user_active(self, obj: AccessAPI) -> bool:
        return obj.user.is_active
    
    def get_warehouse(self, obj: AccessAPI) -> str:
        return obj.warehouse.slug
    
    def get_warehouse_title(self, obj: AccessAPI) -> str:
        return obj.warehouse.title

    def get_warehouse_active(self, obj: AccessAPI) -> bool:
        return obj.warehouse.is_active()

    class Meta:
        model = AccessAPI
        fields = ("slug",
                  "user", "user_first_name", "user_last_name", "user_email", "user_active",
                  "warehouse", "warehouse_title", "warehouse_active",
                  "user_type", "active", "created_time")

class AccessAPICreateSerializer(BaseModelSerializer, serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    warehouse = serializers.SlugRelatedField(slug_field="slug", queryset=Warehouse.objects.all())
    
    class Meta:
        model = AccessAPI
        fields = ("user", "warehouse", "user_type", "active")