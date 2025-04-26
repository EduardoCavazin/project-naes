from django.urls import path
from .views import (
    ExpenseCreate, ExpenseList, ExpenseUpdate, ExpenseDelete,
    PaymentMethodList, PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodDelete,
    # repita para Cheque, Category, PaymentMethod, Account…
)

urlpatterns = [
    #Despesas
    path('despesas/', ExpenseList.as_view(),    name='expense-list'),
    path('despesas/novo/', ExpenseCreate.as_view(),  name='expense-create'),
    path('despesas/<int:pk>/editar/', ExpenseUpdate.as_view(), name='expense-update'),
    path('despesas/<int:pk>/excluir/', ExpenseDelete.as_view(), name='expense-delete'),
    
    #Métodos de pagamento
    path('metodos/',                PaymentMethodList.as_view(),    name='paymentmethod-list'),
    path('metodos/novo/',           PaymentMethodCreate.as_view(),  name='paymentmethod-create'),
    path('metodos/<int:pk>/editar/', PaymentMethodUpdate.as_view(), name='paymentmethod-update'),
    path('metodos/<int:pk>/excluir/', PaymentMethodDelete.as_view(), name='paymentmethod-delete'),
]
