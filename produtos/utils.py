import os
from django.conf import settings
from .models import Produto

from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm


def gerar_etiquetas_bematech(produtos_quantidade):
    """
    PRÉVIA + IMPRESSÃO GRÁFICA
    Etiqueta JOIAS – Elgin Bematech
    TAMANHO REAL: 52mm x 10mm
    """

    pasta = os.path.join(settings.MEDIA_ROOT, "etiquetas")
    os.makedirs(pasta, exist_ok=True)

    pdf_path = os.path.join(pasta, "etiquetas_bematech_52x10mm.pdf")

    # 🔑 TAMANHO REAL DA ETIQUETA
    LARGURA = 52 * mm
    ALTURA = 10 * mm

    c = canvas.Canvas(pdf_path, pagesize=(LARGURA, ALTURA))

    for produto_id, quantidade in produtos_quantidade:
        produto = Produto.objects.get(id=produto_id)

        for _ in range(quantidade):

            # 🔹 BORDA (somente para visualização)
            c.setLineWidth(0.25)
            c.rect(0.5, 0.5, LARGURA - 1, ALTURA - 1)

            # ===============================
            # LINHA SUPERIOR: CÓDIGO + NOME
            # ===============================
            c.setFont("Helvetica", 6)
            c.drawString(
                1.5 * mm,
                ALTURA - 3 * mm,
                f"Cód.: {produto.codigo_barras}"
            )

            c.setFont("Helvetica-Bold", 6)
            c.drawRightString(
                LARGURA - 1.5 * mm,
                ALTURA - 3 * mm,
                produto.nome[:22]
            )

            # ===============================
            # BARCODE (ESQUERDA)
            # ===============================
            barcode = code128.Code128(
                produto.codigo_barras,
                barHeight=5.5 * mm,
                barWidth=0.38
            )

            barcode.drawOn(
                c,
                -3 * mm,
                1.2 * mm
            )

            # ===============================
            # PREÇO (DIREITA / INFERIOR)
            # ===============================
            c.setFont("Helvetica-Bold", 7.5)
            c.drawRightString(
                LARGURA - 1.5 * mm,
                1.4 * mm,
                f"R$ {produto.preco:.2f}"
            )

            c.showPage()

    c.save()
    return pdf_path

