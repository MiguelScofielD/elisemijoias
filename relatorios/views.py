from django.shortcuts import render
from django.db.models import Sum
from vendas.models import Venda
from clientes.models import Cliente
from vendas.models import ItemVenda



def vendas_por_periodo(request):
    inicio = request.GET.get("inicio")
    fim = request.GET.get("fim")

    vendas = Venda.objects.filter(status="finalizada")

    if inicio and fim:
        vendas = vendas.filter(data__date__range=[inicio, fim])

    total = vendas.aggregate(Sum("total"))["total__sum"] or 0

    return render(
        request,
        "relatorios/vendas_periodo.html",
        {
            "vendas": vendas,
            "total": total,
            "inicio": inicio,
            "fim": fim,
        }
    )

def vendas_por_cliente(request):
    cliente_id = request.GET.get("cliente")

    vendas = Venda.objects.filter(status="finalizada")
    clientes = Cliente.objects.all()

    if cliente_id:
        vendas = vendas.filter(cliente_id=cliente_id)

    total = vendas.aggregate(Sum("total"))["total__sum"] or 0

    return render(
        request,
        "relatorios/vendas_cliente.html",
        {
            "vendas": vendas,
            "clientes": clientes,
            "total": total,
            "cliente_id": cliente_id,
        }
    )

def produtos_mais_vendidos(request):
    produtos = (
        ItemVenda.objects
        .values("produto__nome")
        .annotate(total_vendido=Sum("quantidade"))
        .order_by("-total_vendido")
    )

    return render(
        request,
        "relatorios/produtos_mais_vendidos.html",
        {
            "produtos": produtos
        }
    )

