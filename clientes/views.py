from django.shortcuts import render, redirect
from .models import Cliente

def cadastrar_cliente(request):
    if request.method == "POST":
        Cliente.objects.create(
            nome=request.POST.get("nome"),
            telefone=request.POST.get("telefone"),
            email=request.POST.get("email"),
            cpf=request.POST.get("cpf"),
        )
        return redirect("clientes:cadastrar_cliente")

    return render(request, "clientes/cadastrar_cliente.html")
