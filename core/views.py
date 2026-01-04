from django.db import models
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

from vendas.models import Venda
from produtos.models import Produto
from financeiro.models import ContaReceber

LIMITE_VENDAS_DASHBOARD = 10


def dashboard(request):
    # ===== DATAS NO HORÁRIO LOCAL =====
    agora = timezone.localtime()

    inicio_dia = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    fim_dia = inicio_dia + timedelta(days=1)

    inicio_mes = inicio_dia.replace(day=1)
    if inicio_mes.month == 12:
        fim_mes = inicio_mes.replace(year=inicio_mes.year + 1, month=1)
    else:
        fim_mes = inicio_mes.replace(month=inicio_mes.month + 1)

    # ===== PRODUTOS =====
    total_produtos = Produto.objects.count()
    estoque_baixo = Produto.objects.filter(
        estoque__lte=models.F("estoque_minimo")
    ).count()

    # ===== VENDAS =====
    total_hoje = (
        Venda.objects
        .filter(
            data__gte=inicio_dia,
            data__lt=fim_dia,
            status="finalizada"
        )
        .aggregate(Sum("total"))["total__sum"] or 0
    )

    total_mes = (
        Venda.objects
        .filter(
            data__gte=inicio_mes,
            data__lt=fim_mes,
            status="finalizada"
        )
        .aggregate(Sum("total"))["total__sum"] or 0
    )

    qtd_vendas = Venda.objects.filter(status="finalizada").count()

    # ===== CONTAS A RECEBER =====
    contas_abertas = ContaReceber.objects.all()
    total_receber = sum(
        conta.saldo() for conta in contas_abertas if conta.saldo() > 0
    )

    # ===== ÚLTIMAS VENDAS =====
    
    ultimas_vendas = (
        Venda.objects
        .select_related("cliente")
        .prefetch_related("itens__produto")
        .order_by("-data")[:LIMITE_VENDAS_DASHBOARD]
    )

    return render(
        request,
        "core/dashboard.html",
        {
            "total_hoje": total_hoje,
            "total_mes": total_mes,
            "qtd_vendas": qtd_vendas,
            "total_receber": total_receber,
            "ultimas_vendas": ultimas_vendas,
            "total_produtos": total_produtos,
            "estoque_baixo": estoque_baixo,
        }
    )
