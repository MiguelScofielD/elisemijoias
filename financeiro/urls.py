from django.urls import path
from . import views

app_name = "financeiro"

urlpatterns = [
    path("contas/", views.contas_receber, name="contas_receber"),
]
