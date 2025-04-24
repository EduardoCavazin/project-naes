from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from .models import Expense

class ExpenseCreate(CreateView):
    model = Expense
    fields = ['description','value','date','user','category','payment_method','account']
    template_name = 'core/form.html'
    success_url = reverse_lazy('expense-list')
    extra_context = {'titulo': 'Cadastrar Despesa'}

class ExpenseList(ListView):
    model = Expense
    template_name = 'core/list.html'
    extra_context = {'titulo': 'Lista de Despesas'}

class ExpenseUpdate(UpdateView):
    model = Expense
    fields = ExpenseCreate.fields
    template_name = 'core/form.html'
    success_url = reverse_lazy('expense-list')
    extra_context = {'titulo': 'Editar Despesa'}

class ExpenseDelete(DeleteView):
    model = Expense
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('expense-list')
    extra_context = {'titulo': 'Excluir Despesa'}
