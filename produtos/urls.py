from django.urls import path
from . import views

app_name = "produtos"

urlpatterns = [
    path("etiquetas/", views.etiquetas_produtos, name="etiquetas_produtos"),
]
