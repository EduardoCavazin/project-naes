from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name        = models.CharField("Nome", max_length=100)
    description = models.TextField("Descrição", blank=True)

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name        = models.CharField("Método", max_length=100)
    description = models.TextField("Descrição", blank=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    identifier = models.CharField("Identificador", max_length=50)
    balance    = models.DecimalField("Saldo", max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.identifier} ({self.user.username})"


class Transaction(models.Model):
    """Modelo abstrato para Expense e Cheque"""
    TRANSACTION_TYPES = [
        ('expense', 'Despesa'),
        ('cheque',  'Cheque'),
    ]
    type  = models.CharField("Tipo", max_length=10, choices=TRANSACTION_TYPES)
    value = models.DecimalField("Valor", max_digits=12, decimal_places=2)
    date  = models.DateField("Data")
    user  = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")

    class Meta:
        abstract = True


class Expense(Transaction):
    name        = models.CharField("Nome", max_length=100)
    description    = models.CharField("Descrição", max_length=200)
    category       = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Categoria")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, verbose_name="Método de Pagamento")
    account        = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name="Conta")
    
    def __str__(self):
        return self.name


class Cheque(Transaction):
    number            = models.CharField("Número", max_length=50)
    issue_date        = models.DateField("Emissão")
    compensation_date = models.DateField("Compensação")
    recipient         = models.CharField("Beneficiário", max_length=200)
    account           = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name="Conta")
