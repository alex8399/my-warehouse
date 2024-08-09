from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView, CreateAPIView

from .serializers import AccessAPISerializer, AccessAPICreateSerializer
from .models import AccessAPI
from .permissions import AccessAPIPermission


class CreateAccessAPIView(CreateAPIView):
    serializer_class = AccessAPICreateSerializer
    permission_classes = (AccessAPIPermission,)


class AccessApiRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = AccessAPI
    serializer_class = AccessAPISerializer
    lookup_field = 'slug'
    permission_classes = (AccessAPIPermission,)
