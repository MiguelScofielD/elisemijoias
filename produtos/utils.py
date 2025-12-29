from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def gerar_etiqueta(produto):
    codigo = produto.codigo_barras

    barcode = Code128(codigo, writer=ImageWriter())
    barcode_path = f"media/barcodes/{codigo}"
    barcode.save(barcode_path)

    pdf_path = f"media/etiquetas/{codigo}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)

    c.drawString(100, 750, produto.nome)
    c.drawString(100, 730, f"R$ {produto.preco}")
    c.drawImage(f"{barcode_path}.png", 100, 650, width=200, height=50)

    c.save()

    return pdf_path
