from django.urls import path

from .views import (
    WarehouseCreateView, WarehouseRetrieveUpdateDestroyView, GoodListView, GoodRetrieveUpdateDestroyView,
    GoodCreateView, GoodLogListView, AccessAPIListView, ShipmentsListView, GoodLogListView, WarehouseLogListView,
)

urlpatterns = [
    path('warehouses/<slug:slug>/goods/', GoodListView.as_view()),
    path('warehouses/<slug:slug>/logs/', WarehouseLogListView.as_view()),
    path('warehouses/<slug:slug>/access-apis/', AccessAPIListView.as_view()),
    path('warehouses/<slug:slug>/shipments/', ShipmentsListView.as_view()),
    path('warehouses/<slug:slug>/', WarehouseRetrieveUpdateDestroyView.as_view()),
    path('warehouses/', WarehouseCreateView.as_view()),
    path('goods/<slug:slug>/logs/', GoodLogListView.as_view()),
    path('goods/<slug:slug>/', GoodRetrieveUpdateDestroyView.as_view()),
    path('goods/', GoodCreateView.as_view()),
]
