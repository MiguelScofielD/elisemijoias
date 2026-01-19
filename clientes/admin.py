from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "endereco","telefone", "email", "cpf")
    search_fields = ("nome", "endereco","telefone", "email", "cpf")
