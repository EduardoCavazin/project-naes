from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import (
    UsuarioCadastroForm, 
    UsuarioLoginForm, 
    UsuarioAlterarSenhaForm,
    UsuarioResetSenhaForm
)

# View para logout customizado
def custom_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('index')

# View para registro de usuários
class RegisterView(CreateView):
    model = User
    form_class = UsuarioCadastroForm  # Usando formulário personalizado
    template_name = 'user/register.html'  # Template específico para registro
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        # Salvar o usuário
        user = form.save()
        
        # Fazer login automático após cadastro
        login(self.request, user)
        
        # Mensagem de sucesso
        messages.success(self.request, f'Usuário {user.username} cadastrado com sucesso!')
        
        # Redirecionar para página inicial ou dashboard
        return redirect('index')  # ou 'user-dashboard' quando criarmos
    
    def form_invalid(self, form):
        # Adicionar mensagem de erro
        messages.error(self.request, 'Erro no cadastro. Verifique os dados informados.')
        return super().form_invalid(form)
