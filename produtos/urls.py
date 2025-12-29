from django.urls import path
from . import views

app_name = "produtos"

urlpatterns = [
    path("etiquetas/", views.etiquetas_produtos, name="etiquetas_produtos"),
]
urlpatterns += [
    path("cadastrar/", views.cadastrar_produto, name="cadastrar_produto"),
]
urlpatterns += [
    path("etiquetas/selecao/", views.selecionar_etiquetas, name="selecionar_etiquetas"),
    path("etiquetas/gerar/", views.gerar_etiquetas_selecionadas, name="gerar_etiquetas"),
    path("estoque/", views.listar_produtos, name="listar_produtos"),

]
