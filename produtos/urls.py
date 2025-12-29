from django.urls import path
from . import views

urlpatterns = [
    path("etiqueta/<int:produto_id>/", views.etiqueta_produto),
]
