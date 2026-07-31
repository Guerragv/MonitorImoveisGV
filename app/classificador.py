def identificar_tipo_imovel(texto):

    texto = texto.lower()


    if "apartamento" in texto:
        return "Apartamento"

    if "casa" in texto:
        return "Casa"

    if "kitnet" in texto or "quitinete" in texto:
        return "Kitnet"

    if "loja" in texto:
        return "Loja"

    if "sala" in texto:
        return "Sala"

    if "lote" in texto:
        return "Lote"

    if "terreno" in texto:
        return "Terreno"

    return "Outros"



def identificar_negocio(texto):

    texto = texto.lower()


    if "aluguel" in texto or "alugar" in texto:
        return "Aluguel"


    if "venda" in texto or "vender" in texto:
        return "Venda"


    return "Outros"