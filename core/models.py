from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name        = models.CharField("Nome", max_length=100)
    description = models.TextField("Descrição", blank=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Usuário")

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField("Método", max_length=100)
    description = models.TextField("Descrição", blank=True)
    supports_installments = models.BooleanField("Suporta Parcelamento", default=False)
    max_installments = models.PositiveSmallIntegerField("Número Máximo de Parcelas", default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Usuário")
    
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
    name = models.CharField("Nome", max_length=100)
    description = models.CharField("Descrição", max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Categoria")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, verbose_name="Método de Pagamento")
    account = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name="Conta")
    installments = models.PositiveSmallIntegerField("Número de Parcelas", default=1)
    installment_number = models.PositiveSmallIntegerField("Parcela Atual", default=1)
    parent_expense = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, 
                                      related_name='child_expenses', verbose_name="Despesa Original")
    
    def __str__(self):
        return self.name


class Cheque(Transaction):
    CHEQUE_STATUS = [
        ('pending', 'Pendente'),
        ('cashed', 'Compensado'),
        ('canceled', 'Cancelado'),
    ]
    number = models.CharField("Número", max_length=50)
    issue_date = models.DateField("Emissão")
    compensation_date = models.DateField("Compensação")
    recipient = models.CharField("Beneficiário", max_length=200)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name="Conta")
    status = models.CharField("Status", max_length=10, choices=CHEQUE_STATUS, default='pending')
    
    def __str__(self):
        return f"Cheque {self.number} - {self.recipient}"
    
    def save(self, *args, **kwargs):
        # Garantir que o tipo seja sempre 'cheque'
        self.type = 'cheque'
        # Usar a data de compensação como data da transação para fins contábeis
        self.date = self.compensation_date
        super().save(*args, **kwargs)
    
    def mark_as_cashed(self):
        """Marca o cheque como compensado e atualiza o saldo da conta"""
        if self.status != 'cashed':
            self.status = 'cashed'
            self.save()
    
    def cancel(self):
        """Cancela o cheque"""
        self.status = 'canceled'
        self.save()
