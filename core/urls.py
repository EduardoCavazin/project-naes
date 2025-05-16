from django.urls import path
from .views import (
    ExpenseCreate, ExpenseList, ExpenseUpdate, ExpenseDelete,
    PaymentMethodList, PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodDelete,
    ChequeList, ChequeCreate, ChequeUpdate, ChequeDelete,
    CategoryList, CategoryCreate, CategoryUpdate, CategoryDelete,
    AccountList, AccountCreate, AccountUpdate, AccountDelete,
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
    
    #Cheques
    path('cheques/',                ChequeList.as_view(),    name='cheque-list'),
    path('cheques/novo/',           ChequeCreate.as_view(),  name='cheque-create'),
    path('cheques/<int:pk>/editar/', ChequeUpdate.as_view(), name='cheque-update'),
    path('cheques/<int:pk>/excluir/', ChequeDelete.as_view(), name='cheque-delete'),
    
    #Categorias
    path('categorias/',                CategoryList.as_view(),    name='category-list'),
    path('categorias/nova/',           CategoryCreate.as_view(),  name='category-create'),
    path('categorias/<int:pk>/editar/', CategoryUpdate.as_view(), name='category-update'),
    path('categorias/<int:pk>/excluir/', CategoryDelete.as_view(), name='category-delete'),
    
    #Contas
    path('contas/',                AccountList.as_view(),    name='account-list'),
    path('contas/nova/',           AccountCreate.as_view(),  name='account-create'),
    path('contas/<int:pk>/editar/', AccountUpdate.as_view(), name='account-update'),
    path('contas/<int:pk>/excluir/', AccountDelete.as_view(), name='account-delete'),
]
