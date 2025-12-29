from django.contrib import messages
from produtos.models import Produto
from django.shortcuts import render, redirect, get_object_or_404
from .utils import calcular_totais


def nova_venda(request):
    carrinho = request.session.get("carrinho", {})
    return render(request, "vendas/nova_venda.html", {"carrinho": carrinho})


def adicionar_por_codigo(request):
    codigo = request.POST.get("codigo_barras")

    try:
        produto = Produto.objects.get(codigo_barras=codigo)
    except Produto.DoesNotExist:
        return redirect("vendas:nova_venda")

    carrinho = request.session.get("carrinho", {})

    pid = str(produto.id)  # ✅ REGRA DE OURO

    if pid in carrinho:
        carrinho[pid]["quantidade"] += 1
    else:
        carrinho[pid] = {
            "produto_id": produto.id,
            "codigo_barras": produto.codigo_barras,  # só informativo
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

    return redirect("vendas:ver_carrinho")



def limpar_carrinho(request):
    request.session["carrinho"] = {}
    request.session.modified = True
    return redirect("vendas:ver_carrinho")

