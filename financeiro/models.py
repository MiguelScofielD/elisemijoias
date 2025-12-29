from django.db import models

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
