from django.urls import path

from .views import  CreateAccessAPIView, AccessApiRetrieveUpdateDestroyView

urlpatterns = [
    path('access-apis/<slug:slug>/', AccessApiRetrieveUpdateDestroyView.as_view()),
    path('access-apis/',  CreateAccessAPIView.as_view()),
]
