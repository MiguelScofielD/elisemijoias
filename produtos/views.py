from django.http import FileResponse
from .models import Produto
from .utils import gerar_etiqueta

def etiqueta_produto(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    pdf = gerar_etiqueta(produto)
    return FileResponse(open(pdf, "rb"), content_type="application/pdf")
