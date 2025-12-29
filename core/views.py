from django.db import models
from django.db.models import Sum
from django.shortcuts import render
from django.utils.timezone import now

from vendas.models import Venda
from produtos.models import Produto
from financeiro.models import ContaReceber
from django.db.models import Count



def dashboard(request):
    hoje = now().date()

    total_produtos = Produto.objects.count()
    estoque_baixo = Produto.objects.filter(
        estoque__lte=models.F("estoque_minimo")
    ).count()
    # Vendas
    total_hoje = (
        Venda.objects
        .filter(data__date=hoje, status="finalizada")
        .aggregate(Sum("total"))["total__sum"] or 0
    )

    total_mes = (
        Venda.objects
        .filter(data__year=hoje.year, data__month=hoje.month, status="finalizada")
        .aggregate(Sum("total"))["total__sum"] or 0
    )

    qtd_vendas = Venda.objects.filter(status="finalizada").count()

    # Produtos com estoque baixo
    produtos_baixo_estoque = Produto.objects.filter(
        estoque__lte=models.F("estoque_minimo")
    )

    contas_abertas = ContaReceber.objects.all()

    total_receber = sum(
        conta.saldo() for conta in contas_abertas if conta.saldo() > 0
    )


    # Últimas vendas
    ultimas_vendas = Venda.objects.order_by("-data")[:5]

    return render(
        request,
        "core/dashboard.html",
        {
            "total_hoje": total_hoje,
            "total_mes": total_mes,
            "qtd_vendas": qtd_vendas,
            "produtos_baixo_estoque": produtos_baixo_estoque,
            "total_receber": total_receber,
            "ultimas_vendas": ultimas_vendas,
            "total_produtos": total_produtos,
            "estoque_baixo": estoque_baixo,
        }
    )
