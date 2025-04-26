from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Expense, PaymentMethod

# ——— EXPENSE ———

class ExpenseCreate(CreateView):
    model = Expense
    fields = ['description','value','date','user','category','payment_method','account']
    template_name = 'core/form_expense.html'
    success_url = reverse_lazy('expense-list')
    extra_context = {'titulo': 'Cadastrar Despesa'}

class ExpenseList(ListView):
    model = Expense
    template_name = 'core/list_expense.html'
    extra_context = {
    'titulo': 'Lista de Despesas',
    'create_url_name': 'expense-create',
    'create_button_label': 'Nova Despesa'
    }

class ExpenseUpdate(UpdateView):
    model = Expense
    fields = ExpenseCreate.fields
    template_name = 'core/form_expense.html'
    success_url = reverse_lazy('expense-list')
    extra_context = {'titulo': 'Editar Despesa'}

class ExpenseDelete(DeleteView):
    model = Expense
    template_name = 'core/confirm_delete_expense.html'
    success_url = reverse_lazy('expense-list')
    extra_context = {'titulo': 'Excluir Despesa'}


# ——— PAYMENT METHOD ———

class PaymentMethodList(ListView):
    model = PaymentMethod
    template_name = 'core/list.html'
    extra_context = {'titulo': 'Lista de Métodos de Pagamento'}

class PaymentMethodCreate(CreateView):
    model = PaymentMethod
    fields = ['name','description']
    template_name = 'core/form.html'
    success_url = reverse_lazy('paymentmethod-list')
    extra_context = {'titulo': 'Cadastrar Método de Pagamento'}

class PaymentMethodUpdate(UpdateView):
    model = PaymentMethod
    fields = ['name','description']
    template_name = 'core/form.html'
    success_url = reverse_lazy('paymentmethod-list')
    extra_context = {'titulo': 'Editar Método de Pagamento'}

class PaymentMethodDelete(DeleteView):
    model = PaymentMethod
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('paymentmethod-list')
    extra_context = {'titulo': 'Excluir Método de Pagamento'}
