import os
from django.conf import settings
from .models import Produto

from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm, cm

from escpos.printer import Win32Raw

def gerar_previa_etiqueta_bematech(produtos_quantidade):
    """
    Prévia fiel da etiqueta Bematech
    52mm x 10mm
    """

    pasta = os.path.join(settings.MEDIA_ROOT, "etiquetas")
    os.makedirs(pasta, exist_ok=True)

    pdf_path = os.path.join(pasta, "previa_etiquetas_bematech.pdf")

    LARGURA = 52 * mm
    ALTURA = 10 * mm

    c = canvas.Canvas(pdf_path, pagesize=(LARGURA, ALTURA))

    for produto_id, quantidade in produtos_quantidade:
        produto = Produto.objects.get(id=produto_id)

        for _ in range(quantidade):

            # BORDA (só para prévia)
            c.setLineWidth(0.3)
            c.rect(0.5, 0.5, LARGURA - 1, ALTURA - 1)

            # CÓDIGO
            c.setFont("Helvetica", 6)
            c.drawString(1.5 * mm, ALTURA - 3.5 * mm, f"Cód.: {produto.codigo_barras}")

            # NOME
            c.setFont("Helvetica-Bold", 6)
            c.drawRightString(
                LARGURA - 1.5 * mm,
                ALTURA - 3.5 * mm,
                produto.nome[:22]
            )

            # BARCODE GRANDE À ESQUERDA
            barcode = code128.Code128(
                produto.codigo_barras,
                barHeight=4.5 * mm,
                barWidth=0.6
            )

            barcode.drawOn(
                c,
                -5 * mm,
                1.2 * mm
            )

            # PREÇO
            c.setFont("Helvetica-Bold", 8)
            c.drawRightString(
                LARGURA - 1.5 * mm,
                1.2 * mm,
                f"R$ {produto.preco}"
            )

            c.showPage()

    c.save()
    return pdf_path

def imprimir_etiqueta_bematech(produto):
    """
    Modelo de etiqueta JOIAS – Bematech
    Aproxima 100% do FastReport antigo
    """

    # 🔴 NOME EXATO da impressora no Windows
    p = Win32Raw("BEMATECH")

    # ======================
    # LINHA 1 – CÓDIGO + NOME
    # ======================
    codigo = f"Cód.: {produto.codigo_barras}"
    nome = produto.nome[:22]

    # 48 colunas → empurra nome pra direita
    linha1 = codigo.ljust(24) + nome.rjust(24)
    p.set(align="left", bold=True)
    p.text(linha1 + "\n")

    # ======================
    # CÓDIGO DE BARRAS
    # ======================
    p.barcode(
        produto.codigo_barras,
        "CODE128",
        width=3,     # largura das barras (AJUSTE FINO)
        height=55,   # altura
        pos="left",
        function_type="A"
    )
    p.text("\n")

    # ======================
    # PREÇO + UNIDADE
    # ======================
    preco = f"R$ {produto.preco:.2f} UN"
    p.set(align="right", bold=True, width=1, height=1)
    p.text(preco + "\n")

    # ======================
    # CORTE
    # ======================
    p.cut()