from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from django.conf import settings
from .models import Produto


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
    produtos_quantidade = [(produto_id, quantidade), ...]
    """
    pasta = os.path.join(settings.MEDIA_ROOT, "etiquetas")
    os.makedirs(pasta, exist_ok=True)

    pdf_path = os.path.join(pasta, "etiquetas_selecionadas.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)

    largura, altura = A4
    x = 40
    y = altura - 80

    for produto_id, quantidade in produtos_quantidade:
        produto = Produto.objects.get(id=produto_id)

        barcode = Code128(produto.codigo_barras, writer=ImageWriter())
        barcode_path = os.path.join(pasta, f"{produto.id}")
        barcode.save(barcode_path)

        for _ in range(quantidade):
            c.setFont("Helvetica", 9)
            c.drawString(x, y, produto.nome)
            c.drawString(x, y - 12, f"R$ {produto.preco}")

            c.drawImage(
                f"{barcode_path}.png",
                x,
                y - 60,
                width=120,
                height=40
            )

            y -= 120

            if y < 100:
                c.showPage()
                y = altura - 80

    c.save()
    return pdf_path
