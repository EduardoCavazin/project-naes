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
            
            # Dados para o gráfico de despesas mensais do usuário (OTIMIZADO)
            today = datetime.date.today()
            current_year = today.year
            
            # Uma única query com agregação por mês (em vez de 12 queries)
            monthly_data = Expense.objects.filter(
                user=user,
                date__year=current_year
            ).values(
                'date__month'
            ).annotate(
                total=Sum('value')
            ).order_by('date__month')
            
            # Criar array com 12 posições (janeiro a dezembro)
            monthly_expenses = [0] * 12
            for item in monthly_data:
                month_index = item['date__month'] - 1  # Janeiro = índice 0
                monthly_expenses[month_index] = float(item['total']) if item['total'] else 0
            
            # Se não há dados mensais, usar dados de exemplo  
            if not any(monthly_expenses):
                monthly_expenses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            
            context['monthly_expenses_data'] = json.dumps(monthly_expenses, ensure_ascii=False)
            
            # Dados para o gráfico de distribuição por categoria do usuário (OTIMIZADO)
            # Uma única query com JOIN + agregação (em vez de N queries)
            category_stats = Expense.objects.filter(
                user=user
            ).values(
                'category__name'
            ).annotate(
                total=Sum('value')
            ).order_by('-total')
            
            category_data = []
            category_labels = []
            
            for stat in category_stats:
                if stat['total'] and stat['category__name']:
                    category_data.append(float(stat['total']))
                    category_labels.append(stat['category__name'])
            
            # Se não há dados de categoria, usar dados de exemplo
            if not category_data:
                category_data = [0]
                category_labels = ['Nenhuma despesa cadastrada']
            
            context['category_data'] = json.dumps(category_data, ensure_ascii=False)
            context['category_labels'] = json.dumps(category_labels, ensure_ascii=False)
            
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
            ], ensure_ascii=False)
            context['category_data'] = json.dumps([850, 450, 380, 290, 220, 180], ensure_ascii=False)
            context['category_labels'] = json.dumps([
                'Alimentação', 'Transporte', 'Saúde', 
                'Lazer', 'Educação', 'Outros'
            ], ensure_ascii=False)
        
        return context

class AboutView(TemplateView):
    template_name = "paginasweb/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
