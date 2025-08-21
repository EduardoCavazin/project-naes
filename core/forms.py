from django import forms
from .models import Expense, PaymentMethod, Cheque
import datetime
import json
from decimal import Decimal, InvalidOperation


class BrazilianCurrencyField(forms.CharField):
    """Campo personalizado para valores monetários brasileiros"""
    
    def to_python(self, value):
        """Converte o valor do campo para um número Python"""
        if value in self.empty_values:
            return None
            
        if isinstance(value, (int, float, Decimal)):
            return Decimal(str(value))
            
        # Processar string com formatação brasileira
        if isinstance(value, str):
            # Remover formatação
            value = value.replace('R$', '').replace(' ', '').strip()
            
            if not value:
                return None
            
            # Substituir vírgula por ponto para decimal
            if ',' in value:
                # Formato brasileiro: 1.500,50
                parts = value.split(',')
                if len(parts) == 2:
                    integer_part = parts[0].replace('.', '')  # Remove separadores de milhares
                    decimal_part = parts[1]
                    value = f"{integer_part}.{decimal_part}"
            else:
                # Se só tem pontos, decidir se é separador de milhares ou decimal
                if '.' in value:
                    parts = value.split('.')
                    if len(parts) == 2 and len(parts[1]) <= 2:
                        # Provavelmente decimal: 15.50
                        pass  # Manter como está
                    else:
                        # Separador de milhares: 1.500 -> 1500
                        value = value.replace('.', '')
        
        try:
            return Decimal(value)
        except (InvalidOperation, TypeError, ValueError):
            raise forms.ValidationError("Informe um valor monetário válido.")
    
    def validate(self, value):
        super().validate(value)
        if value is not None and value < 0:
            raise forms.ValidationError("O valor não pode ser negativo.")


class ExpenseForm(forms.ModelForm):
    installments = forms.IntegerField(
        min_value=1,
        initial=1,
        required=False,
        label="Número de Parcelas",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_installments'})
    )
    
    # Usar o campo personalizado para valor
    value = BrazilianCurrencyField(
        label="Valor",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'R$ 0,00',
        })
    )
    
    class Meta:
        model = Expense
        fields = [
            'name',
            'description',
            'value',
            'date',
            'user',
            'category',
            'payment_method',
            'account',
            'installments',
        ]
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['date'].initial = datetime.date.today()
        
        # Filtrar categorias: próprias do usuário + categorias públicas
        if user:
            from django.db.models import Q
            from .models import Category
            self.fields['category'].queryset = Category.objects.filter(
                Q(user=user) | Q(is_public=True)
            ).distinct()
        
        payment_methods = PaymentMethod.objects.all()
        supports_installments = {}
        for method in payment_methods:
            supports_installments[method.id] = {
                'supports': method.supports_installments,
                'max': method.max_installments
            }
        
        self.fields['payment_method'].widget.attrs['data-installment-methods'] = json.dumps(supports_installments)

class ChequeForm(forms.ModelForm):
    # Usar o campo personalizado para valor
    value = BrazilianCurrencyField(
        label="Valor",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'R$ 0,00',
        })
    )
    
    class Meta:
        model = Cheque
        fields = [
            'number',
            'value',
            'issue_date',
            'compensation_date',
            'recipient',
            'account',
            'user',
            'status',
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'compensation_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['issue_date'].initial = datetime.date.today()
            self.fields['compensation_date'].initial = datetime.date.today()
