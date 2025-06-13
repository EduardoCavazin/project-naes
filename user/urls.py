from django.urls import path
from django.contrib.auth.views import LoginView, PasswordChangeView
from . import views  # Importar nossas views customizadas

urlpatterns = [
    
    path("login/", LoginView.as_view(
        template_name = 'core/account/form.html',
        extra_context = {'title': 'Login'}),
    name="login"),
    
    path("register/", views.RegisterView.as_view(), name="register"),
    
    path("logout/", views.custom_logout, name="logout"),  # Usando nossa view customizada
    
    path("password_change/", PasswordChangeView.as_view(
        template_name = 'core/account/form.html',
        extra_context = {'title': 'Alterar Senha'}),
    name="password_change"),

]
