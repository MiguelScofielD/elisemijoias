from django.urls import path
from . import views

app_name = "financeiro"

urlpatterns = [
    path("contas/", views.contas_receber, name="contas_receber"),
]
urlpatterns += [
    path("contas/pagar/<int:conta_id>/", views.pagar_conta, name="pagar_conta"),
]
urlpatterns += [
    path("cliente/<int:cliente_id>/", views.historico_cliente, name="historico_cliente"),
]
urlpatterns += [
    path("clientes/", views.lista_clientes, name="lista_clientes"),
]