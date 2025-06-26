from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Expense, PaymentMethod, Cheque, Account, Category
from .forms import ExpenseForm, ChequeForm
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import calendar

# ——— EXPENSE ———

class ExpenseCreate(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'core/expense/form.html'
    success_url = reverse_lazy('expense-list')
    extra_context = {'titulo': 'Cadastrar Despesa'}
    
    def form_valid(self, form):
        expense = form.save(commit=False)
        expense.user = self.request.user  # Atribuir usuário automaticamente
        
        installments = form.cleaned_data.get('installments') or 1
        
        payment_method = expense.payment_method
        if not payment_method.supports_installments:
            installments = 1
        elif installments > payment_method.max_installments:
            installments = payment_method.max_installments
        
        if installments == 1:
            return super().form_valid(form)
        
        value_per_installment = expense.value / installments
        original_date = expense.date
        
        expense.installments = installments
        expense.installment_number = 1
        expense.value = value_per_installment
        expense.name = f"{expense.name} (1/{installments})"
        expense.save()
        
        for i in range(2, installments + 1):
            next_month = original_date.month + (i - 1)
            next_year = original_date.year + ((next_month - 1) // 12)
            next_month = ((next_month - 1) % 12) + 1
            next_date = datetime.date(next_year, next_month, min(original_date.day, calendar.monthrange(next_year, next_month)[1]))
            
            Expense.objects.create(
                name=f"{expense.name.split(' (')[0]} ({i}/{installments})",
                description=expense.description,
                value=value_per_installment,
                date=next_date,
                type=expense.type,
                user=expense.user,
                category=expense.category,
                payment_method=expense.payment_method,
                account=expense.account,
                installments=installments,
                installment_number=i,
                parent_expense=expense
            )
        
        return HttpResponseRedirect(self.success_url)

class ExpenseList(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'core/expense/list.html'
    extra_context = {
    'titulo': 'Lista de Despesas',
    'create_url_name': 'expense-create',
    'create_button_label': 'Nova Despesa'
    }
    
    def get_queryset(self):
        # Mostrar apenas despesas do usuário logado
        return Expense.objects.filter(user=self.request.user)

class ExpenseUpdate(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'core/expense/form.html'
    success_url = reverse_lazy('expense-list')
    extra_context = {'titulo': 'Editar Despesa'}
    
    def get_queryset(self):
        # Permitir editar apenas despesas do usuário logado
        return Expense.objects.filter(user=self.request.user)

class ExpenseDelete(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'core/expense/confirm_delete.html'
    success_url = reverse_lazy('expense-list')
    extra_context = {'titulo': 'Excluir Despesa'}
    
    def get_queryset(self):
        # Permitir excluir apenas despesas do usuário logado
        return Expense.objects.filter(user=self.request.user)

# ——— CHEQUE ———

class ChequeCreate(LoginRequiredMixin, CreateView):
    model = Cheque
    form_class = ChequeForm
    template_name = 'core/cheque/form.html'
    success_url = reverse_lazy('cheque-list')
    extra_context = {'titulo': 'Cadastrar Cheque'}
    
    def form_valid(self, form):
        cheque = form.save(commit=False)
        cheque.user = self.request.user  # Atribuir usuário automaticamente
        return super().form_valid(form)

class ChequeList(LoginRequiredMixin, ListView):
    model = Cheque
    template_name = 'core/cheque/list.html'
    extra_context = {
        'titulo': 'Lista de Cheques',
        'create_url_name': 'cheque-create',
        'create_button_label': 'Novo Cheque'
    }
    
    def get_queryset(self):
        # Mostrar apenas cheques do usuário logado
        return Cheque.objects.filter(user=self.request.user)

class ChequeUpdate(LoginRequiredMixin, UpdateView):
    model = Cheque
    form_class = ChequeForm
    template_name = 'core/cheque/form.html'
    success_url = reverse_lazy('cheque-list')
    extra_context = {'titulo': 'Editar Cheque'}
    
    def get_queryset(self):
        # Permitir editar apenas cheques do usuário logado
        return Cheque.objects.filter(user=self.request.user)

class ChequeDelete(LoginRequiredMixin, DeleteView):
    model = Cheque
    template_name = 'core/cheque/confirm_delete.html'
    success_url = reverse_lazy('cheque-list')
    extra_context = {'titulo': 'Excluir Cheque'}
    
    def get_queryset(self):
        # Permitir excluir apenas cheques do usuário logado
        return Cheque.objects.filter(user=self.request.user)

# ——— PAYMENT METHOD ———

class PaymentMethodCreate(LoginRequiredMixin, CreateView):
    model = PaymentMethod
    fields = ['name', 'description', 'supports_installments', 'max_installments']
    template_name = 'core/payment_method/form.html'
    success_url = reverse_lazy('paymentmethod-list')
    extra_context = {'titulo': 'Cadastrar Método de Pagamento'}

class PaymentMethodList(LoginRequiredMixin, ListView):
    model = PaymentMethod
    template_name = 'core/payment_method/list.html'
    extra_context = {
        'titulo': 'Lista de Métodos de Pagamento',
        'create_url_name': 'paymentmethod-create',
        'create_button_label': 'Novo Método'
    }

class PaymentMethodUpdate(LoginRequiredMixin, UpdateView):
    model = PaymentMethod
    fields = ['name', 'description', 'supports_installments', 'max_installments']
    template_name = 'core/payment_method/form.html'
    success_url = reverse_lazy('paymentmethod-list')
    extra_context = {'titulo': 'Editar Método de Pagamento'}

class PaymentMethodDelete(LoginRequiredMixin, DeleteView):
    model = PaymentMethod
    template_name = 'core/paymentmethod/confirm_delete.html'
    success_url = reverse_lazy('paymentmethod-list')
    extra_context = {'titulo': 'Excluir Método de Pagamento'}

# ——— CATEGORY ———

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'core/category/form.html'
    success_url = reverse_lazy('category-list')
    extra_context = {'titulo': 'Cadastrar Categoria'}

class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'core/category/list.html'
    extra_context = {
        'titulo': 'Lista de Categorias',
        'create_url_name': 'category-create',
        'create_button_label': 'Nova Categoria'
    }

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'core/category/form.html'
    success_url = reverse_lazy('category-list')
    extra_context = {'titulo': 'Editar Categoria'}

class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'core/category/confirm_delete.html'
    success_url = reverse_lazy('category-list')
    extra_context = {'titulo': 'Excluir Categoria'}

# ——— ACCOUNT ———

class AccountCreate(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['identifier', 'balance']
    template_name = 'core/account/form.html'
    success_url = reverse_lazy('account-list')
    extra_context = {'titulo': 'Cadastrar Conta'}
    
    def form_valid(self, form):
        account = form.save(commit=False)
        account.user = self.request.user  # Atribuir usuário automaticamente
        return super().form_valid(form)

class AccountList(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'core/account/list.html'
    extra_context = {
        'titulo': 'Lista de Contas',
        'create_url_name': 'account-create',
        'create_button_label': 'Nova Conta'
    }
    
    def get_queryset(self):
        # Mostrar apenas contas do usuário logado
        return Account.objects.filter(user=self.request.user)

class AccountUpdate(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['identifier', 'balance']
    template_name = 'core/account/form.html'
    success_url = reverse_lazy('account-list')
    extra_context = {'titulo': 'Editar Conta'}
    
    def get_queryset(self):
        # Permitir editar apenas contas do usuário logado
        return Account.objects.filter(user=self.request.user)

class AccountDelete(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'core/account/confirm_delete.html'
    success_url = reverse_lazy('account-list')
    extra_context = {'titulo': 'Excluir Conta'}
    
    def get_queryset(self):
        # Permitir excluir apenas contas do usuário logado
        return Account.objects.filter(user=self.request.user)

