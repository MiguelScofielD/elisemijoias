from django.http import FileResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages

from .models import Produto, gerar_codigo_barras
from .utils import gerar_etiquetas_bematech


# ======================================================
# ETIQUETAS – PRÉVIA / IMPRESSÃO (PDF)
# ======================================================
def previa_etiquetas_bematech(request):
    """
    Gera o PDF de etiquetas Bematech
    Serve tanto para pré-visualização quanto impressão
    """
    if request.method != "POST":
        return redirect("produtos:selecionar_etiquetas")

    produtos_ids = request.POST.getlist("produto")
    quantidades = request.POST

    if not produtos_ids:
        messages.warning(request, "Selecione ao menos um produto.")
        return redirect("produtos:selecionar_etiquetas")

    produtos_quantidade = []

    for pid in produtos_ids:
        qtd = int(quantidades.get(f"quantidade_{pid}", 1))
        produtos_quantidade.append((pid, qtd))

    pdf = gerar_etiquetas_bematech(produtos_quantidade)

    return FileResponse(
        open(pdf, "rb"),
        content_type="application/pdf"
    )


# ======================================================
# CADASTRO DE PRODUTO
# ======================================================
def cadastrar_produto(request):
    if request.method == "POST":
        Produto.objects.create(
            nome=request.POST.get("nome"),
            codigo_barras=gerar_codigo_barras(),
            preco=request.POST.get("preco"),
            estoque=request.POST.get("estoque"),
            estoque_minimo=request.POST.get("estoque_minimo"),
            imagem=request.FILES.get("imagem")
        )

        messages.success(request, "Produto cadastrado com sucesso.")
        return redirect("produtos:listar_produtos")

    return render(request, "produtos/cadastrar_produto.html")


# ======================================================
# SELEÇÃO DE ETIQUETAS
# ======================================================
def selecionar_etiquetas(request):
    busca = request.GET.get("q", "")
    produtos = Produto.objects.all()

    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) |
            Q(codigo_barras__icontains=busca)
        )

    return render(
        request,
        "produtos/etiquetas_selecao.html",
        {
            "produtos": produtos,
            "busca": busca,
        }
    )


# ======================================================
# LISTAGEM DE PRODUTOS
# ======================================================
def listar_produtos(request):
    busca = request.GET.get("q", "")
    produtos = Produto.objects.all()

    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) |
            Q(codigo_barras__icontains=busca)
        )

    return render(
        request,
        "produtos/listar_produtos.html",
        {
            "produtos": produtos,
            "busca": busca
        }
    )


# ======================================================
# IMPRESSÃO (MESMO PDF DA PRÉVIA)
# ======================================================
def imprimir_etiquetas_bematech(request):
    """
    Impressão via PDF + driver do Windows
    (Elgin Bematech)
    """
    if request.method != "POST":
        return redirect("produtos:selecionar_etiquetas")

    produtos_ids = request.POST.getlist("produto")
    quantidades = request.POST

    if not produtos_ids:
        messages.warning(request, "Selecione ao menos um produto.")
        return redirect("produtos:selecionar_etiquetas")

    produtos_quantidade = []
    total_etiquetas = 0

    for pid in produtos_ids:
        qtd = int(quantidades.get(f"quantidade_{pid}", 1))
        produtos_quantidade.append((pid, qtd))
        total_etiquetas += qtd

    pdf = gerar_etiquetas_bematech(produtos_quantidade)

    messages.success(
        request,
        f"🖨️ {total_etiquetas} etiqueta(s) geradas. Use Ctrl+P para imprimir na Bematech."
    )

    return FileResponse(
        open(pdf, "rb"),
        content_type="application/pdf"
    )
