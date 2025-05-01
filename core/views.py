from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Expense, PaymentMethod
from .forms import ExpenseForm
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
        # Obter os dados do formulário
        expense = form.save(commit=False)
        installments = form.cleaned_data.get('installments') or 1
        
        # Verificar se o método de pagamento suporta parcelamento
        payment_method = expense.payment_method
        if not payment_method.supports_installments:
            installments = 1
        elif installments > payment_method.max_installments:
            installments = payment_method.max_installments
        
        # Se for apenas uma parcela, salvar normalmente
        if installments == 1:
            return super().form_valid(form)
        
        # Caso contrário, criar várias despesas
        value_per_installment = expense.value / installments
        original_date = expense.date
        
        # Salvar a despesa original como a primeira parcela
        expense.installments = installments
        expense.installment_number = 1
        expense.value = value_per_installment
        expense.name = f"{expense.name} (1/{installments})"
        expense.save()
        
        # Criar as demais parcelas
        for i in range(2, installments + 1):
            # Calcular a data da parcela (um mês após a anterior)
            next_month = original_date.month + (i - 1)
            next_year = original_date.year + ((next_month - 1) // 12)
            next_month = ((next_month - 1) % 12) + 1
            next_date = datetime.date(next_year, next_month, min(original_date.day, calendar.monthrange(next_year, next_month)[1]))
            
            # Criar uma nova despesa para esta parcela
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
