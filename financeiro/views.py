from django.shortcuts import render
from django.utils.timezone import now
from .models import ContaReceber

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
