from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import ContaReceber
from decimal import Decimal
from .models import ContaReceber, PagamentoRecebido
from clientes.models import Cliente



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
    contas = ContaReceber.objects.filter( venda__cliente=cliente ).prefetch_related("pagamentos") 
    return render( request, "financeiro/historico_cliente.html", { "cliente": cliente, "contas": contas } )
