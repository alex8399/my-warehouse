from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView

from django.shortcuts import get_object_or_404

from apps.api.models import AccessAPI
from apps.api.serializers import AccessAPISerializer
from apps.warehouses.models import Warehouse
from apps.accounts.models import User
from utils.paginations import StandartListPagination

from .serializers import UserSerializer, UserRegisterSerializer
from .permissions import UserPermission


class UserAccessAPIsListView(ListAPIView):
    serializer_class = AccessAPISerializer
    pagination_class = StandartListPagination
    lookup_field = 'username'
    permission_classes = (UserPermission,)

    def get_queryset(self):
        field_value = self.kwargs.get(self.lookup_field)
        kwargs = {self.lookup_field: field_value}
        user = get_object_or_404(User, **kwargs)
        queryset = user.get_access_APIs()
        return queryset


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)
    lookup_field = 'username'

class UserCreateView(CreateAPIView):
    serializer_class = UserRegisterSerializer