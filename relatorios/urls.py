from django.urls import path
from . import views

app_name = "relatorios"

urlpatterns = [
    path("vendas-periodo/", views.vendas_por_periodo, name="vendas_periodo"),
    path("vendas-cliente/", views.vendas_por_cliente, name="vendas_cliente"),
    path("produtos-mais-vendidos/", views.produtos_mais_vendidos, name="produtos_mais_vendidos"),
]
