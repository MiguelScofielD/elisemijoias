def calcular_totais(carrinho):
    total = 0
    for item in carrinho.values():
        item["subtotal"] = item["preco"] * item["quantidade"]
        total += item["subtotal"]
    return total
