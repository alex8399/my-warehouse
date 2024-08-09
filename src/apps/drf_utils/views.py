from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect


class UserLoginView(LoginView):
    template_name = 'api/login.html'
    next_page = 'login'


def user_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')
