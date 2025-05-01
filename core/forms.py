from django import forms
from .models import Expense
import datetime

class ExpenseForm(forms.ModelForm):
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
            
    def clean_value(self):
        """
        Converte o valor formatado (R$ 1.234,56) para decimal (1234.56)
        """
        value = self.cleaned_data.get('value')
        if isinstance(value, str):
            # Remove R$, espaços e substitui vírgula por ponto
            value = value.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
        return value
