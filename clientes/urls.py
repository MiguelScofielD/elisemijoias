from django.urls import path
from . import views

app_name = "clientes"

urlpatterns = [
    path("cadastrar/", views.cadastrar_cliente, name="cadastrar_cliente"),
]
