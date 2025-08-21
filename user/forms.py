from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm, 
    PasswordChangeForm,
    PasswordResetForm
)
from django.contrib.auth.models import User
from django import forms


# Formulário personalizado para LOGIN
class UsuarioLoginForm(AuthenticationForm):
    
    username = forms.CharField(
        max_length=254,
        label="Nome de usuário",
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome de usuário',
            'class': 'form-control'
        }),
        help_text="Digite seu nome de usuário."
    )
    
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha',
            'class': 'form-control'
        }),
        help_text="Digite sua senha."
    )
    
    class Meta:
        model = User
        fields = ['username', 'password']


# Formulário personalizado para CADASTRO DE USUÁRIOS
# A herança é feita para poder tornar o email único e obrigatório
# E outros campos, se necessário
class UsuarioCadastroForm(UserCreationForm):

    username = forms.CharField(
        max_length=150,
        label="Nome de usuário",
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome de usuário',
            'class': 'form-control'
        }),
    )
    
    email = forms.EmailField(
        required=True,
        label="Email", 
        widget=forms.EmailInput(attrs={
            'placeholder': 'seu-email@exemplo.com',
            'class': 'form-control'
        }),
    )
    
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
            'class': 'form-control'
        }),
    )
    
    password2 = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha',
            'class': 'form-control'
        }),
    )

    # Define o model e os fields que vão aparecer na tela
    class Meta:
        model = User
        # Esses dois passwords são para verificar se as senhas são iguais
        fields = ['username', 'email', 'password1', 'password2']

    # O método clean no forms serve de validação para os campos
    def clean_email(self):
        # recebe o email do formulário
        email = self.cleaned_data.get('email')
        # Verifica se já existe algum usuário com este email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email


# Formulário personalizado para ALTERAR SENHA
class UsuarioAlterarSenhaForm(PasswordChangeForm):
    
    old_password = forms.CharField(
        label="Senha atual",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha atual',
            'class': 'form-control'
        }),
        help_text="Digite sua senha atual para confirmar."
    )
    
    new_password1 = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Nova senha',
            'class': 'form-control'
        }),
        help_text="Sua nova senha deve ter pelo menos 8 caracteres."
    )
    
    new_password2 = forms.CharField(
        label="Confirmar nova senha",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme a nova senha',
            'class': 'form-control'
        }),
        help_text="Digite a mesma senha novamente para confirmação."
    )
    
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


# Formulário personalizado para RESET DE SENHA
class UsuarioResetSenhaForm(PasswordResetForm):
    
    email = forms.EmailField(
        max_length=254,
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'seu-email@exemplo.com',
            'class': 'form-control'
        }),
        help_text="Digite o email associado à sua conta."
    )
    
    class Meta:
        model = User
        fields = ['email']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verificar se o email existe no sistema
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Não existe usuário cadastrado com este email.")
        return email
