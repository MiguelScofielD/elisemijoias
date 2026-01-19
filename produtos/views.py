from django.http import FileResponse
from .models import Produto
from django.shortcuts import render, redirect
from .models import Produto
from .models import Produto, gerar_codigo_barras
from django.db.models import Q
from .utils import imprimir_etiqueta_bematech
from .models import Produto
from .utils import gerar_previa_etiqueta_bematech

def previa_etiquetas_bematech(request):
    if request.method != "POST":
        return redirect("produtos:selecionar_etiquetas")

    produtos_ids = request.POST.getlist("produto")
    quantidades = request.POST

    produtos_quantidade = []

    for pid in produtos_ids:
        qtd = int(quantidades.get(f"quantidade_{pid}", 1))
        produtos_quantidade.append((pid, qtd))

    pdf = gerar_previa_etiqueta_bematech(produtos_quantidade)
    return FileResponse(open(pdf, "rb"), content_type="application/pdf")


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
        return redirect("produtos:listar_produtos")

    return render(request, "produtos/cadastrar_produto.html")

def selecionar_etiquetas(request):
    busca = request.GET.get("q", "")
    selecionados = request.GET.getlist("produto")  # 🔴 ATENÇÃO AQUI

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
            "selecionados": selecionados,
        }
    )

# def gerar_etiquetas_selecionadas(request):
#     if request.method != "POST":
#         return redirect("produtos:selecionar_etiquetas")

#     produtos_ids = request.POST.getlist("produto")
#     quantidades = request.POST

#     produtos_quantidade = []

#     for pid in produtos_ids:
#         qtd = int(quantidades.get(f"quantidade_{pid}", 1))
#         produtos_quantidade.append((pid, qtd))

#     pdf = gerar_etiquetas_personalizadas(produtos_quantidade)

#     return FileResponse(open(pdf, "rb"), content_type="application/pdf")

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

def imprimir_etiquetas_bematech(request):
    if request.method != "POST":
        return redirect("produtos:selecionar_etiquetas")

    produtos_ids = request.POST.getlist("produto")
    quantidades = request.POST

    for pid in produtos_ids:
        produto = Produto.objects.get(id=pid)
        qtd = int(quantidades.get(f"quantidade_{pid}", 1))

        for _ in range(qtd):
            imprimir_etiqueta_bematech(produto)

    return redirect("produtos:selecionar_etiquetas")