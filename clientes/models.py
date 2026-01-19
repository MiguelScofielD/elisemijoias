from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255, blank=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    cpf = models.CharField(max_length=14, blank=True)

    def __str__(self):
        return self.nome
