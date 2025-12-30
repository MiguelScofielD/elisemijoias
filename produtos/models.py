from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=150)
    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)
    codigo_barras = models.CharField(max_length=20, unique=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    estoque_minimo = models.IntegerField(default=0)

    imagem = models.ImageField(
        upload_to="produtos/",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nome

def gerar_codigo_barras():
    ultimo = Produto.objects.order_by("id").last()
    if not ultimo:
        return "000001"
    return str(int(ultimo.codigo_barras) + 1).zfill(6)
