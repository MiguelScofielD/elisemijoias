from django.db import models

class Venda(models.Model):
    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    data = models.DateTimeField(auto_now_add=True)

    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    desconto = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    status = models.CharField(
        max_length=20,
        choices=[('aberta', 'Aberta'), ('finalizada', 'Finalizada')]
    )


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey('produtos.Produto', on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
