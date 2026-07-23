from config.filtros import (
    VALOR_MAXIMO,
    CIDADE,
    TIPO,
    FINALIDADE
)


def aprovado(imovel):

    titulo = imovel.get("titulo", "")
    localizacao = imovel.get("localizacao", "")
    valor = imovel.get("valor", "")


    # Verifica cidade
    texto_localizacao = (
        titulo + " " + localizacao
    ).lower()


    if CIDADE.lower() not in texto_localizacao:
        return False


    # Verifica tipo do imóvel
    if TIPO.lower() not in titulo.lower():
        return False


    # Extrai valor do aluguel
    valor_limpo = (
        valor
        .replace("Aluguel", "")
        .replace("R$", "")
        .replace(".", "")
        .replace(",", ".")
        .strip()
    )


    try:
        valor_numero = float(valor_limpo)

    except:
        return False


    # Verifica valor máximo
    if valor_numero > VALOR_MAXIMO:
        return False


    return True