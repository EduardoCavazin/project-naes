import django_filters
from django import forms
from .models import Expense, Cheque, Category, PaymentMethod, Account


class ExpenseFilter(django_filters.FilterSet):
    # icontains: busca por nome (contém texto, case-insensitive)
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Nome contém',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite parte do nome'})
    )

    # exact: filtro exato por categoria
    category = django_filters.ModelChoiceFilter(
        lookup_expr='exact',
        label='Categoria exata',
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # gte: data maior ou igual
    date_from = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        label='Data a partir de',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    # lte: valor menor ou igual
    value_max = django_filters.NumberFilter(
        field_name='value',
        lookup_expr='lte',
        label='Valor máximo',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 100.50'})
    )

    # Filtros adicionais úteis
    payment_method = django_filters.ModelChoiceFilter(
        queryset=PaymentMethod.objects.all(),
        label='Método de pagamento',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    account = django_filters.ModelChoiceFilter(
        queryset=Account.objects.all(),
        label='Conta',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Expense
        fields = ['name', 'category', 'date_from', 'value_max', 'payment_method', 'account']


class ChequeFilter(django_filters.FilterSet):
    # icontains: busca por beneficiário (contém texto, case-insensitive)
    recipient = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Beneficiário contém',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite parte do nome do beneficiário'})
    )

    # exact: status exato
    status = django_filters.ChoiceFilter(
        choices=Cheque.CHEQUE_STATUS,
        lookup_expr='exact',
        label='Status exato',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # gte: data de compensação maior ou igual
    compensation_date_from = django_filters.DateFilter(
        field_name='compensation_date',
        lookup_expr='gte',
        label='Compensação a partir de',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    # lte: valor menor ou igual
    value_max = django_filters.NumberFilter(
        field_name='value',
        lookup_expr='lte',
        label='Valor máximo',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 500.00'})
    )

    # Filtros adicionais úteis
    account = django_filters.ModelChoiceFilter(
        queryset=Account.objects.all(),
        label='Conta',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    number = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Número do cheque',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o número'})
    )

    class Meta:
        model = Cheque
        fields = ['recipient', 'status', 'compensation_date_from', 'value_max', 'account', 'number']