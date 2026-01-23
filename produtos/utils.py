import os
from django.conf import settings
from .models import Produto

from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm


def gerar_etiquetas_bematech(produtos_quantidade):
    """
    ETIQUETA JOIAS – Elgin Bematech (driver gráfico)
    Tamanho compatível com o driver: 70mm x 40mm

    Este PDF serve tanto para:
    - Pré-visualização
    - Impressão final (Ctrl+P no Windows)
    """

    # 📁 Pasta de saída
    pasta = os.path.join(settings.MEDIA_ROOT, "etiquetas")
    os.makedirs(pasta, exist_ok=True)

    pdf_path = os.path.join(pasta, "etiquetas_bematech.pdf")

    # 📐 TAMANHO DO PAPEL (IGUAL AO DRIVER)
    LARGURA = 70 * mm
    ALTURA = 40 * mm

    c = canvas.Canvas(pdf_path, pagesize=(LARGURA, ALTURA))

    for produto_id, quantidade in produtos_quantidade:
        produto = Produto.objects.get(id=produto_id)

        for _ in range(quantidade):

            # =========================
            # BORDA (APENAS VISUAL)
            # =========================
            c.setLineWidth(0.3)
            c.rect(1, 1, LARGURA - 2, ALTURA - 2)

            # =========================
            # LINHA SUPERIOR
            # =========================
            c.setFont("Helvetica", 8)
            c.drawString(
                5 * mm,
                ALTURA - 8 * mm,
                f"Cód.: {produto.codigo_barras}"
            )

            c.setFont("Helvetica-Bold", 8)
            c.drawString(
                30 * mm,
                ALTURA - 8 * mm,
                produto.nome[:22]
            )

            # =========================
            # CÓDIGO DE BARRAS
            # =========================
            barcode = code128.Code128(
                produto.codigo_barras,
                barHeight=10 * mm,
                barWidth=0.6
            )

            barcode.drawOn(
                c,
                5 * mm,
                12 * mm
            )

            # =========================
            # PREÇO
            # =========================
            c.setFont("Helvetica-Bold", 10)
            c.drawString(
                30 * mm,
                12 * mm,
                f"R$ {produto.preco:.2f} UN"
            )

            c.showPage()

    c.save()
    return pdf_path
