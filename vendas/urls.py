from django.urls import path
from . import views

app_name = "vendas"

urlpatterns = [
    path("nova/", views.nova_venda, name="nova_venda"),
    path("adicionar/", views.adicionar_por_codigo, name="adicionar_codigo"),
    path("carrinho/", views.ver_carrinho, name="ver_carrinho"),
    path("carrinho/adicionar/<int:produto_id>/", views.adicionar_ao_carrinho, name="adicionar_ao_carrinho"),
    path("carrinho/remover/<int:produto_id>/", views.remover_do_carrinho, name="remover_do_carrinho"),
    path("carrinho/limpar/", views.limpar_carrinho, name="limpar_carrinho"),
]
