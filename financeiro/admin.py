from django.contrib import admin
from .models import ContaReceber

@admin.register(ContaReceber)
class ContaReceberAdmin(admin.ModelAdmin):
    list_display = ("id", "venda", "valor", "vencimento", "pago")
    list_filter = ("pago", "vencimento")
    readonly_fields = ("pago",)
