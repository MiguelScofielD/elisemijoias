from django.db import models
from django.db.models import Sum


class ContaReceber(models.Model):
    venda = models.OneToOneField(
        'vendas.Venda',
        on_delete=models.CASCADE
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    vencimento = models.DateField()
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"Venda {self.venda_id} - R$ {self.valor}"
    
    def total_pago(self):
        return self.pagamentos.aggregate(
            total=Sum("valor")
        )["total"] or 0

    def saldo(self):
        return self.valor - self.total_pago()

    def status(self):
        if self.saldo() <= 0:
            return "Paga"
        return "Em aberto"
    
    

class PagamentoRecebido(models.Model):
    conta = models.ForeignKey(
        ContaReceber,
        related_name="pagamentos",
        on_delete=models.CASCADE
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pagamento R$ {self.valor} - Conta {self.conta.id}"
