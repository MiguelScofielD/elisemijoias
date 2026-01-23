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
    CONTEÚDO ROTACIONADO PARA IMPRIMIR CERTO
    """

    pasta = os.path.join(settings.MEDIA_ROOT, "etiquetas")
    os.makedirs(pasta, exist_ok=True)

    pdf_path = os.path.join(pasta, "etiquetas_bematech_52x10mm.pdf")

    # 🔴 PAPEL VERTICAL (IMPORTANTE)
    LARGURA = 10 * mm
    ALTURA = 52 * mm

    c = canvas.Canvas(pdf_path, pagesize=(LARGURA, ALTURA))

    for produto_id, quantidade in produtos_quantidade:
        produto = Produto.objects.get(id=produto_id)

        for _ in range(quantidade):

            c.saveState()

            # ==========================
            # 🔁 ROTAÇÃO CORRETA
            # ==========================
            c.translate(LARGURA, 0)
            c.rotate(90)

            largura_r = ALTURA   # 52mm
            altura_r = LARGURA   # 10mm

            # (opcional) BORDA DE TESTE
            c.setLineWidth(0.3)
            c.rect(0.5, 0.5, largura_r - 1, altura_r - 1)

            # TEXTO SUPERIOR
            c.setFont("Helvetica", 6)
            c.drawString(
                1.5 * mm,
                altura_r - 3 * mm,
                f"Cód.: {produto.codigo_barras}"
            )

            c.setFont("Helvetica-Bold", 6)
            c.drawRightString(
                largura_r - 1.5 * mm,
                altura_r - 3 * mm,
                produto.nome[:22]
            )

            # BARCODE À ESQUERDA
            barcode = code128.Code128(
                produto.codigo_barras,
                barHeight=5.5 * mm,
                barWidth=0.38
            )

            barcode.drawOn(
                c,
                1.2 * mm,
                1.2 * mm
            )

            # PREÇO
            c.setFont("Helvetica-Bold", 7.5)
            c.drawRightString(
                largura_r - 1.5 * mm,
                1.2 * mm,
                f"R$ {produto.preco:.2f}"
            )

            c.restoreState()
            c.showPage()

    c.save()
    return pdf_path




