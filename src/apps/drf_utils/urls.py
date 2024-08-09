from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import UserLoginView, user_logout_view
from manage import DEBUG

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

if DEBUG:
    urlpatterns += [
        path('debug/login/', UserLoginView.as_view(), name='login'),
        path('debug/logout/', user_logout_view, name='logout'),
    ]
