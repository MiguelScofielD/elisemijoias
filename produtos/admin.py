from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "codigo_barras",
        "preco",
        "estoque",
        "estoque_minimo",
    )
    search_fields = ("nome", "codigo_barras")
    list_filter = ("estoque",)
