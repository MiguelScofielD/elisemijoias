from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo_barras = models.CharField(max_length=50, unique=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    estoque_minimo = models.IntegerField(default=1)

    def __str__(self):
        return self.nome
