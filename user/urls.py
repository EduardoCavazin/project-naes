from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

urlpatterns = [
    
    path("login/", LoginView.as_view(
        template_name = 'core/account/form.html',
        extra_context = {'title': 'Login'}),
    name="login"),
    path("logout/", LogoutView.as_view(http_method_names=['get', 'post']), name="logout"),
    path("password_change/", PasswordChangeView.as_view(
        template_name = 'core/account/form.html',
        extra_context = {'title': 'Alterar Senha'}),
    name="password_change"),

]
