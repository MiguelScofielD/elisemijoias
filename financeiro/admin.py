from django.contrib import admin
from .models import ContaReceber

@admin.register(ContaReceber)
class ContaReceberAdmin(admin.ModelAdmin):
    list_display = ("venda", "valor", "vencimento", "pago")
    list_filter = ("pago", "vencimento")
