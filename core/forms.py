from django import forms
from .models import Expense, PaymentMethod, Cheque
import datetime
import json

class ExpenseForm(forms.ModelForm):
    installments = forms.IntegerField(
        min_value=1,
        initial=1,
        required=False,
        label="Número de Parcelas",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_installments'})
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
            'value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'R$ 0,00',
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['date'].initial = datetime.date.today()
        
        payment_methods = PaymentMethod.objects.all()
        supports_installments = {}
        for method in payment_methods:
            supports_installments[method.id] = {
                'supports': method.supports_installments,
                'max': method.max_installments
            }
        
        self.fields['payment_method'].widget.attrs['data-installment-methods'] = json.dumps(supports_installments)
            
    def clean_value(self):
        value = self.cleaned_data.get('value')
        if isinstance(value, str):
            value = value.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
        return value

class ChequeForm(forms.ModelForm):
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
            'value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'R$ 0,00',
            }),
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
            
    def clean_value(self):
        """
        Converte o valor formatado (R$ 1.234,56) para decimal (1234.56)
        """
        value = self.cleaned_data.get('value')
        if isinstance(value, str):
            # Remove R$, espaços e substitui vírgula por ponto
            value = value.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
        return value
