from django.urls import path
from .views import dashboard
from . import views

app_name = "core"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("desligar/", views.desligar_sistema, name="desligar_sistema"),
]
