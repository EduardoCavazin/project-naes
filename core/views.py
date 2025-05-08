from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Expense, PaymentMethod, Cheque, Account, Category
from .forms import ExpenseForm, ChequeForm
import datetime
import calendar

# ——— EXPENSE ———

class ExpenseCreate(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'core/expense/form.html'
    success_url = reverse_lazy('expense-list')
    extra_context = {'titulo': 'Cadastrar Despesa'}
    
    def form_valid(self, form):
        expense = form.save(commit=False)
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

class ExpenseList(ListView):
    model = Expense
    template_name = 'core/expense/list.html'
    extra_context = {
    'titulo': 'Lista de Despesas',
    'create_url_name': 'expense-create',
    'create_button_label': 'Nova Despesa'
    }

class ExpenseUpdate(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'core/expense/form.html'
    success_url = reverse_lazy('expense-list')
    extra_context = {'titulo': 'Editar Despesa'}

class ExpenseDelete(DeleteView):
    model = Expense
    template_name = 'core/expense/confirm_delete.html'
    success_url = reverse_lazy('expense-list')
    extra_context = {'titulo': 'Excluir Despesa'}


# ——— PAYMENT METHOD ———

class PaymentMethodList(ListView):
    model = PaymentMethod
    template_name = 'core/payment_method/list.html'
    extra_context = {
        'titulo': 'Lista de Métodos de Pagamento',
        'create_url_name': 'paymentmethod-create',
        'create_button_label': 'Novo Método'
    }

class PaymentMethodCreate(CreateView):
    model = PaymentMethod
    fields = ['name', 'description', 'supports_installments', 'max_installments']
    template_name = 'core/payment_method/form.html'
    success_url = reverse_lazy('paymentmethod-list')
    extra_context = {'titulo': 'Cadastrar Método de Pagamento'}

class PaymentMethodUpdate(UpdateView):
    model = PaymentMethod
    fields = ['name', 'description', 'supports_installments', 'max_installments']
    template_name = 'core/payment_method/form.html'
    success_url = reverse_lazy('paymentmethod-list')
    extra_context = {'titulo': 'Editar Método de Pagamento'}

class PaymentMethodDelete(DeleteView):
    model = PaymentMethod
    template_name = 'core/payment_method/confirm_delete.html'
    success_url = reverse_lazy('paymentmethod-list')
    extra_context = {'titulo': 'Excluir Método de Pagamento'}

# ——— CHEQUE ———

class ChequeList(ListView):
    model = Cheque
    template_name = 'core/cheque/list.html'
    extra_context = {
        'titulo': 'Lista de Cheques',
        'create_url_name': 'cheque-create',
        'create_button_label': 'Novo Cheque'
    }

class ChequeCreate(CreateView):
    model = Cheque
    form_class = ChequeForm
    template_name = 'core/cheque/form.html'
    success_url = reverse_lazy('cheque-list')
    extra_context = {'titulo': 'Cadastrar Cheque'}
    
    def form_valid(self, form):
        cheque = form.save(commit=False)
        cheque.type = 'cheque'
        
        # Se a data de compensação já passou, marcar como compensado automaticamente
        today = datetime.date.today()
        if cheque.compensation_date <= today and cheque.status == 'pending':
            cheque.status = 'cashed'
            
            # Opcionalmente, atualizar o saldo da conta aqui
            # account = cheque.account
            # account.balance -= cheque.value
            # account.save()
        
        return super().form_valid(form)

class ChequeUpdate(UpdateView):
    model = Cheque
    form_class = ChequeForm
    template_name = 'core/cheque/form.html'
    success_url = reverse_lazy('cheque-list')
    extra_context = {'titulo': 'Editar Cheque'}
    
    def form_valid(self, form):
        cheque = form.save(commit=False)
        original_cheque = Cheque.objects.get(pk=cheque.pk)
        
        # Se o status mudou de pendente para compensado, atualizar saldo
        if original_cheque.status == 'pending' and cheque.status == 'cashed':
            # Opcionalmente, atualizar o saldo da conta aqui
            # account = cheque.account
            # account.balance -= cheque.value
            # account.save()
            pass  # Remova este 'pass' quando implementar a lógica acima
        # Se o status mudou de compensado para cancelado, restaurar saldo
        elif original_cheque.status == 'cashed' and cheque.status == 'canceled':
            # Opcionalmente, restaurar o saldo da conta aqui
            # account = cheque.account
            # account.balance += cheque.value
            # account.save()
            pass  # Remova este 'pass' quando implementar a lógica acima
            
        return super().form_valid(form)

class ChequeDelete(DeleteView):
    model = Cheque
    template_name = 'core/cheque/confirm_delete.html'
    success_url = reverse_lazy('cheque-list')
    extra_context = {'titulo': 'Excluir Cheque'}

# ——— CATEGORY ———

class CategoryList(ListView):
    model = Category
    template_name = 'core/category/list.html'
    extra_context = {
        'titulo': 'Lista de Categorias',
        'create_url_name': 'category-create',
        'create_button_label': 'Nova Categoria'
    }

class CategoryCreate(CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'core/category/form.html'
    success_url = reverse_lazy('category-list')
    extra_context = {'titulo': 'Cadastrar Categoria'}

class CategoryUpdate(UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'core/category/form.html'
    success_url = reverse_lazy('category-list')
    extra_context = {'titulo': 'Editar Categoria'}

class CategoryDelete(DeleteView):
    model = Category
    template_name = 'core/category/confirm_delete.html'
    success_url = reverse_lazy('category-list')
    extra_context = {'titulo': 'Excluir Categoria'}

# ——— ACCOUNT ———

class AccountList(ListView):
    model = Account
    template_name = 'core/account/list.html'
    extra_context = {
        'titulo': 'Lista de Contas',
        'create_url_name': 'account-create',
        'create_button_label': 'Nova Conta'
    }
    
    def get_queryset(self):
        # Filtrar apenas contas do usuário atual
        return Account.objects.filter(user=self.request.user)

class AccountCreate(CreateView):
    model = Account
    fields = ['identifier', 'balance']
    template_name = 'core/account/form.html'
    success_url = reverse_lazy('account-list')
    extra_context = {'titulo': 'Cadastrar Conta'}
    
    def form_valid(self, form):
        account = form.save(commit=False)
        account.user = self.request.user
        return super().form_valid(form)

class AccountUpdate(UpdateView):
    model = Account
    fields = ['identifier', 'balance']
    template_name = 'core/account/form.html'
    success_url = reverse_lazy('account-list')
    extra_context = {'titulo': 'Editar Conta'}
    
    def get_queryset(self):
        # Garantir que usuários só possam editar suas próprias contas
        return Account.objects.filter(user=self.request.user)

class AccountDelete(DeleteView):
    model = Account
    template_name = 'core/account/confirm_delete.html'
    success_url = reverse_lazy('account-list')
    extra_context = {'titulo': 'Excluir Conta'}
    
    def get_queryset(self):
        # Garantir que usuários só possam excluir suas próprias contas
        return Account.objects.filter(user=self.request.user)
