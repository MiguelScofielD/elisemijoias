from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "produtos"

urlpatterns = [
    path("cadastrar/", views.cadastrar_produto, name="cadastrar_produto"),
]

urlpatterns += [
    path("etiquetas/selecao/", views.selecionar_etiquetas, name="selecionar_etiquetas"),
    path("etiquetas/gerar/", views.gerar_etiquetas_selecionadas, name="gerar_etiquetas"),
    path("estoque/", views.listar_produtos, name="listar_produtos"),
    path("etiquetas/imprimir-bematech/", views.imprimir_etiquetas_bematech, name="imprimir_etiquetas_bematech"),
    path("etiquetas/previa-bematech/", views.previa_etiquetas_bematech, name="previa_etiquetas_bematech")

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
