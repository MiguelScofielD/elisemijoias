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

    # def __str__(self):
    #     return f"Venda {self.venda_id} - R$ {self.valor}"
    
    def total_pago(self):
        return sum(p.valor for p in self.pagamentos.all())

    def saldo(self):
        return self.valor - self.total_pago()

    def atualizar_status(self):
        """Atualiza automaticamente o campo pago"""
        self.pago = self.saldo() <= 0
        self.save(update_fields=["pago"])
    
    def __str__(self):
        return f"Conta #{self.id} - Venda {self.venda.id}"
    

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
