from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import ContaReceber
from decimal import Decimal
from .models import ContaReceber, PagamentoRecebido
from clientes.models import Cliente
from django.db.models import Sum
from vendas.models import Venda




def contas_receber(request):
    filtro = request.GET.get("status")

    contas = ContaReceber.objects.all()
    hoje = now().date()

    if filtro == "atrasadas":
        contas = contas.filter(pago=False, vencimento__lt=hoje)
    elif filtro == "pendentes":
        contas = contas.filter(pago=False, vencimento__gte=hoje)

    return render(
        request,
        "financeiro/contas_receber.html",
        {
            "contas": contas,
            "filtro": filtro,
        }
    )

def pagar_conta(request, conta_id):
    conta = ContaReceber.objects.get(id=conta_id)

    if request.method == "POST":
        valor_pago = Decimal(request.POST.get("valor"))

        if valor_pago > 0 and valor_pago <= conta.saldo():
            PagamentoRecebido.objects.create(
                conta=conta,
                valor=valor_pago
            )

            # 🔥 ATUALIZA STATUS AUTOMATICAMENTE
            conta.atualizar_status()

        return redirect("financeiro:contas_receber")

    return render(
        request,
        "financeiro/pagar_conta.html",
        {"conta": conta}
    )

def historico_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)

    vendas = (
        Venda.objects
        .filter(cliente=cliente)
        .prefetch_related(
            "itens__produto",
            "contareceber__pagamentos"
        )
        .order_by("-data")
    )

    return render(
        request,
        "financeiro/historico_cliente.html",
        {
            "cliente": cliente,
            "vendas": vendas
        }
    )

def lista_clientes(request):
    busca = request.GET.get("q", "")

    clientes = Cliente.objects.all()

    if busca:
        clientes = clientes.filter(nome__icontains=busca)

    dados = []

    for cliente in clientes:
        contas = ContaReceber.objects.filter(
            venda__cliente=cliente,
            pago=False
        )

        saldo = contas.aggregate(
            total=Sum("valor")
        )["total"] or 0

        dados.append({
            "cliente": cliente,
            "saldo": saldo
        })

    return render(
        request,
        "financeiro/lista_clientes.html",
        {
            "dados": dados,
            "busca": busca
        }
    )

