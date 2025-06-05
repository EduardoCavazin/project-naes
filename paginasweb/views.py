from django.views.generic import TemplateView
from django.db.models import Sum, Count
from core.models import Expense, Category, Account, Cheque, PaymentMethod
import datetime
import calendar
import json

class IndexView(TemplateView):
    template_name = "paginasweb/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Contagem de registros
        context['total_categories'] = Category.objects.count()
        context['total_accounts'] = Account.objects.count()
        context['total_pending_cheques'] = Cheque.objects.filter(status='pending').count()
        
        # Total de despesas
        total_expenses = Expense.objects.aggregate(total=Sum('value'))
        context['total_expenses'] = total_expenses['total'] or 0
        
        # Dados para o gráfico de despesas mensais
        today = datetime.date.today()
        current_year = today.year
        monthly_expenses = []
        
        # Obtém as despesas mensais para o ano atual
        for month in range(1, 13):
            last_day = calendar.monthrange(current_year, month)[1]
            start_date = datetime.date(current_year, month, 1)
            end_date = datetime.date(current_year, month, last_day)
            
            month_total = Expense.objects.filter(
                date__gte=start_date, 
                date__lte=end_date
            ).aggregate(total=Sum('value'))
            
            monthly_expenses.append(month_total['total'] or 0)
        
        context['monthly_expenses_data'] = json.dumps(monthly_expenses)
        
        # Dados para o gráfico de distribuição por categoria
        categories = Category.objects.all()
        category_data = []
        category_labels = []
        
        for category in categories:
            total = Expense.objects.filter(category=category).aggregate(total=Sum('value'))
            if total['total']:
                category_data.append(float(total['total']))
                category_labels.append(category.name)
        
        context['category_data'] = json.dumps(category_data)
        context['category_labels'] = json.dumps(category_labels)
        
        return context

class AboutView(TemplateView):
    template_name = "paginasweb/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
