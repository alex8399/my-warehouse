from django.urls import path

from .views import (ShipmentCreateView, ShipmentRetrieveUpdateDestroyView, ShipmentItemsListView,
                    ShipmentLogsListView, ItemRetrieveUpdateDestroyView, ItemLogsListView,
                    ItemCreateView)

urlpatterns = [
    path('shipments/<slug:slug>/goods/', ShipmentItemsListView.as_view()),
    path('shipments/<slug:slug>/logs/', ShipmentLogsListView.as_view()),
    path('shipments/<slug:slug>/', ShipmentRetrieveUpdateDestroyView.as_view()),
    path('shipments/', ShipmentCreateView.as_view()),
    path('items/<slug:slug>/logs/', ItemLogsListView.as_view()),
    path('items/<slug:slug>/', ItemRetrieveUpdateDestroyView.as_view()),
    path('items/', ItemCreateView.as_view())
]