from django.views.generic import TemplateView
from django.db.models import Sum, Count, Q
from core.models import Expense, Category, Account, Cheque, PaymentMethod
import datetime
import calendar
import json

class IndexView(TemplateView):
    template_name = "paginasweb/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            # DADOS PERSONALIZADOS DO USUÁRIO LOGADO
            user = self.request.user
            
            # Contagem de registros do usuário
            context['total_categories'] = Category.objects.filter(
                Q(user=user) | Q(is_public=True)
            ).count()
            context['total_accounts'] = Account.objects.filter(user=user).count()
            context['total_pending_cheques'] = Cheque.objects.filter(
                user=user, status='pending'
            ).count()
            
            # Total de despesas do usuário
            total_expenses = Expense.objects.filter(user=user).aggregate(total=Sum('value'))
            total_value = total_expenses['total']
            context['total_expenses'] = float(total_value) if total_value else 0
            
            # Dados para o gráfico de despesas mensais do usuário
            today = datetime.date.today()
            current_year = today.year
            monthly_expenses = []
            
            # Obtém as despesas mensais do usuário para o ano atual
            for month in range(1, 13):
                last_day = calendar.monthrange(current_year, month)[1]
                start_date = datetime.date(current_year, month, 1)
                end_date = datetime.date(current_year, month, last_day)
                
                month_total = Expense.objects.filter(
                    user=user,
                    date__gte=start_date, 
                    date__lte=end_date
                ).aggregate(total=Sum('value'))
                
                # Converter Decimal para float para serialização JSON
                total_value = month_total['total']
                monthly_expenses.append(float(total_value) if total_value else 0)
            
            # Se não há dados mensais, usar dados de exemplo
            if not any(monthly_expenses):
                monthly_expenses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            
            context['monthly_expenses_data'] = json.dumps(monthly_expenses)
            
            # Dados para o gráfico de distribuição por categoria do usuário
            categories = Category.objects.filter(
                Q(user=user) | Q(is_public=True)
            )
            category_data = []
            category_labels = []
            
            for category in categories:
                total = Expense.objects.filter(
                    user=user, category=category
                ).aggregate(total=Sum('value'))
                if total['total']:
                    category_data.append(float(total['total']))
                    category_labels.append(category.name)
            
            # Se não há dados de categoria, usar dados de exemplo
            if not category_data:
                category_data = [0]
                category_labels = ['Nenhuma despesa cadastrada']
            
            context['category_data'] = json.dumps(category_data)
            context['category_labels'] = json.dumps(category_labels)
            
        else:
            # DADOS DEMO PARA USUÁRIOS NÃO LOGADOS
            context['total_categories'] = 12
            context['total_accounts'] = 3
            context['total_pending_cheques'] = 2
            context['total_expenses'] = 3247.89
            
            # Dados demo para gráficos (dados fictícios atraentes)
            context['monthly_expenses_data'] = json.dumps([
                2850, 3100, 2750, 3200, 2900, 3350, 
                3100, 3247, 2950, 3400, 3150, 2800
            ])
            context['category_data'] = json.dumps([850, 450, 380, 290, 220, 180])
            context['category_labels'] = json.dumps([
                'Alimentação', 'Transporte', 'Saúde', 
                'Lazer', 'Educação', 'Outros'
            ])
        
        return context

class AboutView(TemplateView):
    template_name = "paginasweb/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
