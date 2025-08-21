from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView, 
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from . import views  # Importar nossas views customizadas
from .forms import (
    UsuarioLoginForm,
    UsuarioAlterarSenhaForm,
    UsuarioResetSenhaForm
)

urlpatterns = [
    
    # Login usando formulário personalizado
    path("login/", LoginView.as_view(
        template_name='user/login.html',
        form_class=UsuarioLoginForm),
    name="login"),
    
    # Registro usando formulário personalizado
    path("register/", views.RegisterView.as_view(), name="register"),
    
    # Logout usando nossa view customizada
    path("logout/", views.custom_logout, name="logout"),
    
    # Alterar senha usando formulário personalizado
    path("password_change/", PasswordChangeView.as_view(
        template_name='user/password_change.html',
        form_class=UsuarioAlterarSenhaForm,
        success_url=reverse_lazy('index')),
    name="password_change"),
    
    # URLs para reset de senha usando formulário personalizado
    path("password_reset/", PasswordResetView.as_view(
        template_name='user/password_reset.html',
        form_class=UsuarioResetSenhaForm),
    name="password_reset"),
    
    path("password_reset/done/", PasswordResetDoneView.as_view(
        template_name = 'user/password_reset_done.html'),
    name="password_reset_done"),
    
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(
        template_name = 'user/password_reset_confirm.html'),
    name="password_reset_confirm"),
    
    path("reset/done/", PasswordResetCompleteView.as_view(
        template_name = 'user/password_reset_complete.html'),
    name="password_reset_complete"),

]
