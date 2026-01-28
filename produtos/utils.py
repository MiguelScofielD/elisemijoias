import os
from django.conf import settings
from .models import Produto

from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm


def gerar_etiquetas_bematech(produtos_quantidade):
    """
    Etiqueta JOIAS – Elgin Bematech
    PAPEL: 10mm (largura) x 52mm (altura)
    Conteúdo rotacionado e invertido conforme impressão real
    """

    pasta = os.path.join(settings.MEDIA_ROOT, "etiquetas")
    os.makedirs(pasta, exist_ok=True)

    pdf_path = os.path.join(pasta, "etiquetas_bematech_52x10mm.pdf")

    # PDF maior para respeitar altura da impressora
    LARGURA = 70 * mm
    ALTURA = 40 * mm

    c = canvas.Canvas(pdf_path, pagesize=(LARGURA, ALTURA))

    for produto_id, quantidade in produtos_quantidade:
        produto = Produto.objects.get(id=produto_id)

        for _ in range(quantidade):

            c.saveState()

            # ==========================
            # 🔁 ROTAÇÃO BASE (90°)
            # ==========================
            c.translate(LARGURA, 0)
            c.rotate(90)

            largura_r = ALTURA     # área útil horizontal
            altura_r = LARGURA

            # ==========================
            # 🔁 ROTAÇÃO EXTRA (180°)
            # Corrige etiqueta invertida
            # ==========================
            c.translate(largura_r, altura_r)
            c.rotate(180)

            # # ==========================
            # # BORDA (TESTE VISUAL)
            # # ==========================
            # c.setLineWidth(0.3)
            # c.rect(0.5, 0.5, largura_r - 1, altura_r - 1)

            # ==========================
            # 🔄 LINHA SUPERIOR (NOME À ESQUERDA / CÓDIGO À DIREITA)
            # ==========================
            c.setFont("Helvetica-Bold", 8)
            c.drawString(
                21 * mm,
                altura_r - 60 * mm,
                produto.nome[:22]
            )

            c.setFont("Helvetica", 7)
            c.drawRightString(
                largura_r - 24 * mm,
                altura_r - 60 * mm,
                f"Cód.: {produto.codigo_barras}"
            )

            # ==========================
            # 🔄 PREÇO (AGORA À ESQUERDA)
            # ==========================
            c.setFont("Helvetica-Bold", 8)
            c.drawString(
                21 * mm,
                4 * mm,
                f"R$ {produto.preco:.2f}"
            )

            # ==========================
            # 🔄 BARCODE (AGORA À DIREITA)
            # ==========================
            barcode = code128.Code128(
                produto.codigo_barras,
                barHeight=5 * mm,
                barWidth=0.5
            )

            barcode.drawOn(
                c,
                largura_r - 43 * mm,
                3 * mm
            )

            c.restoreState()
            c.showPage()

    c.save()
    return pdf_path




