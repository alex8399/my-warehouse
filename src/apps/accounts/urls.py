from django.urls import path

from .views import UserRetrieveUpdateDestroyView, UserAccessAPIsListView, UserCreateView

urlpatterns = [
    path('accounts/<slug:username>/access-apis/', UserAccessAPIsListView.as_view()),
    path('accounts/<slug:username>/', UserRetrieveUpdateDestroyView.as_view()),
    path('accounts/', UserCreateView.as_view()),
]