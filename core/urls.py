from django.urls import path
from .views import (
    ExpenseCreate, ExpenseList, ExpenseUpdate, ExpenseDelete,
    # repita para Cheque, Category, PaymentMethod, Account…
)

urlpatterns = [
    path('despesas/', ExpenseList.as_view(),    name='expense-list'),
    path('despesas/novo/', ExpenseCreate.as_view(),  name='expense-create'),
    path('despesas/<int:pk>/editar/', ExpenseUpdate.as_view(), name='expense-update'),
    path('despesas/<int:pk>/excluir/', ExpenseDelete.as_view(), name='expense-delete'),
    # …idem para /cheques/, /categorias/, /contas/, /metodos/, etc.
]
