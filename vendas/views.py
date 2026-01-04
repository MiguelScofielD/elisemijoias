from django.contrib import messages
from produtos.models import Produto
from django.shortcuts import render, redirect, get_object_or_404
from .utils import calcular_totais
from django.db import transaction
from clientes.models import Cliente
from vendas.models import Venda, ItemVenda
from financeiro.models import ContaReceber
from clientes.models import Cliente
from decimal import Decimal


def nova_venda(request):
    carrinho = request.session.get("carrinho", {})
    total = calcular_totais(carrinho)

    codigo_invalido = request.session.pop("codigo_invalido", "")

    return render(
        request,
        "vendas/nova_venda.html",
        {
            "carrinho": carrinho,
            "total": total,
            "codigo_invalido": codigo_invalido,
        }
    )



def adicionar_por_codigo(request):
    codigo = (
        request.POST
        .get("codigo_barras", "")
        .replace("\n", "")
        .replace("\r", "")
        .replace("\t", "")
        .strip()
    )

    if not codigo:
        return redirect("vendas:nova_venda")

    try:
        produto = Produto.objects.get(codigo_barras=codigo)
    except Produto.DoesNotExist:
        messages.error(
            request,
            f"Código {codigo} não encontrado no sistema."
        )

        # 🔴 GUARDA O CÓDIGO PARA REEXIBIR
        request.session["codigo_invalido"] = codigo
        return redirect("vendas:nova_venda")

    # ✅ LIMPA SE EXISTIA ERRO ANTERIOR
    request.session.pop("codigo_invalido", None)

    carrinho = request.session.get("carrinho", {})
    pid = str(produto.id)

    if pid in carrinho:
        carrinho[pid]["quantidade"] += 1
    else:
        carrinho[pid] = {
            "produto_id": produto.id,
            "codigo_barras": produto.codigo_barras,
            "nome": produto.nome,
            "preco": float(produto.preco),
            "quantidade": 1,
        }

    request.session["carrinho"] = carrinho
    request.session.modified = True

    return redirect("vendas:nova_venda")




def ver_carrinho(request):
    carrinho = request.session.get("carrinho", {})
    total = calcular_totais(carrinho)

    request.session["carrinho"] = carrinho
    request.session.modified = True

    return render(
        request,
        "vendas/carrinho.html",
        {
            "carrinho": carrinho,
            "total": total
        }
    )

def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if produto.estoque <= 0:
        return redirect("vendas:ver_carrinho")

    carrinho = request.session.get("carrinho", {})

    pid = str(produto.id)  # 🔴 SEMPRE string

    if pid in carrinho:
        carrinho[pid]["quantidade"] += 1
    else:
        carrinho[pid] = {
            "produto_id": produto.id,   # 🔴 GARANTIDO
            "nome": produto.nome,
            "preco": float(produto.preco),
            "quantidade": 1
        }

    request.session["carrinho"] = carrinho
    request.session.modified = True

    return redirect("vendas:ver_carrinho")


def remover_do_carrinho(request, produto_id):
    carrinho = request.session.get("carrinho", {})

    pid = str(produto_id)

    if pid in carrinho:
        del carrinho[pid]

    request.session["carrinho"] = carrinho
    request.session.modified = True

    return redirect("vendas:nova_venda")


def limpar_carrinho(request):
    request.session["carrinho"] = {}
    request.session.modified = True
    return redirect("vendas:ver_carrinho")

def confirmar_venda(request):
    carrinho = request.session.get("carrinho", {})
    clientes = Cliente.objects.all()

    total = sum(item["preco"] * item["quantidade"] for item in carrinho.values())

    return render(
        request,
        "vendas/confirmar_venda.html",
        {
            "carrinho": carrinho,
            "total": total,
            "clientes": clientes,
        }
    )


@transaction.atomic
def finalizar_venda(request):
    carrinho = request.session.get("carrinho", {})

    if not carrinho:
        return redirect("vendas:nova_venda")

    cliente_id = request.POST.get("cliente")
    cliente = Cliente.objects.get(id=cliente_id) if cliente_id else None

    # 🔹 DESCONTO (VALOR FIXO EM R$)
    desconto = Decimal(request.POST.get("desconto") or 0)

    # 🔹 CRIA VENDA
    venda = Venda.objects.create(
        cliente=cliente,
        status="finalizada"
    )

    subtotal = Decimal("0.00")

    # 🔹 ITENS DA VENDA
    for item in carrinho.values():
        produto = Produto.objects.get(id=item["produto_id"])

        if produto.estoque < item["quantidade"]:
            raise Exception("Estoque insuficiente")

        ItemVenda.objects.create(
            venda=venda,
            produto=produto,
            quantidade=item["quantidade"],
            preco_unitario=item["preco"]
        )

        produto.estoque -= item["quantidade"]
        produto.save()

        subtotal += Decimal(item["preco"]) * item["quantidade"]

    # 🔹 GARANTIA DE DESCONTO VÁLIDO
    if desconto < 0:
        desconto = Decimal("0.00")

    if desconto > subtotal:
        desconto = subtotal

    # 🔹 TOTAIS FINAIS
    venda.subtotal = subtotal
    venda.desconto = desconto
    venda.total = subtotal - desconto
    venda.save()

    # 🔹 CONTA A RECEBER (USA TOTAL FINAL)
    prazo = request.POST.get("prazo")
    if prazo == "sim":
        ContaReceber.objects.create(
            venda=venda,
            valor=venda.total,
            vencimento=request.POST.get("vencimento")
        )

    # 🔹 LIMPA CARRINHO
    request.session["carrinho"] = {}
    request.session.modified = True

    return redirect("vendas:nova_venda")
