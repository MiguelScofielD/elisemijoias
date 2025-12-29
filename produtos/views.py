from django.http import FileResponse
from .models import Produto
from .utils import gerar_etiquetas

def etiquetas_produtos(request):
    produtos = Produto.objects.all()
    pdf = gerar_etiquetas(produtos)
    return FileResponse(open(pdf, "rb"), content_type="application/pdf")
