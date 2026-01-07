from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from django.conf import settings
from .models import Produto
from reportlab.lib.units import cm
from reportlab.graphics.barcode import code128


def gerar_etiquetas(produtos):
    """
    Gera um PDF com etiquetas de produtos (em lote)
    """
    pasta = os.path.join(settings.MEDIA_ROOT, "etiquetas")
    os.makedirs(pasta, exist_ok=True)

    pdf_path = os.path.join(pasta, "etiquetas_produtos.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)

    largura, altura = A4

    x = 40
    y = altura - 80

    for produto in produtos:
        # --- gerar código de barras ---
        barcode = Code128(produto.codigo_barras, writer=ImageWriter())
        barcode_path = os.path.join(pasta, f"{produto.id}")
        barcode.save(barcode_path)

        # --- texto ---
        c.setFont("Helvetica", 9)
        c.drawString(x, y, produto.nome)
        c.drawString(x, y - 12, f"R$ {produto.preco}")

        # --- imagem do código de barras ---
        c.drawImage(
            f"{barcode_path}.png",
            x,
            y - 60,
            width=120,
            height=40
        )

        # --- próxima etiqueta ---
        y -= 120

        if y < 100:
            c.showPage()
            y = altura - 80

    c.save()
    return pdf_path

def gerar_etiquetas_personalizadas(produtos_quantidade):
    """
    Etiqueta JOIAS
    5,2 cm x 1,0 cm
    Código de barras GRANDE e À ESQUERDA
    """

    pasta = os.path.join(settings.MEDIA_ROOT, "etiquetas")
    os.makedirs(pasta, exist_ok=True)

    pdf_path = os.path.join(pasta, "etiquetas_joias_52x10mm.pdf")

    # TAMANHO REAL DA ETIQUETA
    LARGURA = 5.2 * cm
    ALTURA = 1.0 * cm

    c = canvas.Canvas(pdf_path, pagesize=(LARGURA, ALTURA))

    for produto_id, quantidade in produtos_quantidade:
        produto = Produto.objects.get(id=produto_id)

        for _ in range(quantidade):

            # BORDA (opcional)
            c.setLineWidth(0.6)
            c.setStrokeColorRGB(0.8, 0.65, 0.2)  # dourado
            c.rect(1, 1, LARGURA - 2, ALTURA - 2)

            # TEXTO SUPERIOR
            c.setFont("Helvetica", 6)
            c.drawString(3, ALTURA - 7, f"Cód.: {produto.codigo_barras}")
            c.drawRightString(LARGURA - 3, ALTURA - 7, produto.nome[:22])

            # 🔥 CÓDIGO DE BARRAS REAL (NÃO IMAGEM)
            barcode = code128.Code128(
                produto.codigo_barras,
                barHeight=0.55 * cm,
                barWidth=0.038 * cm  # controla largura REAL das barras
            )

            barcode.drawOn(
                c,
                -15,     # COLADO À ESQUERDA
                3
            )

            # PREÇO (DIREITA)
            c.setFont("Helvetica-Bold", 7.8)
            c.drawRightString(
                LARGURA - 6,
                3,
                f"R$ {produto.preco}"
            )

            c.showPage()

    c.save()
    return pdf_path

