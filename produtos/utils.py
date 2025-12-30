from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from django.conf import settings
from .models import Produto
from reportlab.lib.units import cm


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
    Gera etiquetas no padrão:
    5,2 cm (largura) x 1,0 cm (altura)
    """
    pasta = os.path.join(settings.MEDIA_ROOT, "etiquetas")
    os.makedirs(pasta, exist_ok=True)

    pdf_path = os.path.join(pasta, "etiquetas_selecionadas.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)

    largura_pagina, altura_pagina = A4

    # MEDIDAS DA ETIQUETA
    ETIQUETA_LARG = 5.2 * cm
    ETIQUETA_ALT = 1.0 * cm

    MARGEM_X = 1 * cm
    MARGEM_Y = 1 * cm

    x = MARGEM_X
    y = altura_pagina - MARGEM_Y - ETIQUETA_ALT

    for produto_id, quantidade in produtos_quantidade:
        produto = Produto.objects.get(id=produto_id)

        barcode = Code128(produto.codigo_barras, writer=ImageWriter())
        barcode_path = os.path.join(pasta, f"barcode_{produto.codigo_barras}")
        barcode.save(barcode_path)

        for _ in range(quantidade):

            # BORDA DA ETIQUETA
            c.setStrokeColorRGB(0.83, 0.69, 0.22)  # dourado
            c.rect(x, y, ETIQUETA_LARG, ETIQUETA_ALT)

            # TEXTO SUPERIOR
            c.setFont("Helvetica", 6)
            c.drawString(
                x + 2,
                y + ETIQUETA_ALT - 8,
                f"Cód.: {produto.codigo_barras}"
            )

            # NOME DO PRODUTO
            c.setFont("Helvetica", 6)
            c.drawString(
                x + 2,
                y + ETIQUETA_ALT - 16,
                produto.nome[:25]
            )

            # CÓDIGO DE BARRAS (MAIOR E MAIS À ESQUERDA)
            c.drawImage(
                f"{barcode_path}.png",
                x + ETIQUETA_LARG - 75,   # afastado do preço
                y + 4,
                width=65,                # um pouco maior
                height=20,
                preserveAspectRatio=True,
                mask="auto"
            )

            # PREÇO (ISOLADO NO CANTO DIREITO)
            c.setFont("Helvetica-Bold", 7.5)
            c.drawRightString(
                x + ETIQUETA_LARG - 3,
                y + 3,
                f"{produto.preco}"
            )


            # PRÓXIMA POSIÇÃO (GRADE)
            x += ETIQUETA_LARG + 5

            if x + ETIQUETA_LARG > largura_pagina:
                x = MARGEM_X
                y -= ETIQUETA_ALT + 5

            if y < MARGEM_Y:
                c.showPage()
                x = MARGEM_X
                y = altura_pagina - MARGEM_Y - ETIQUETA_ALT

    c.save()
    return pdf_path

