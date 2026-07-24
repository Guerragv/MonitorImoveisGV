import yaml
from pathlib import Path


def carregar_config():

    caminho = Path("config/config.yaml")

    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return yaml.safe_load(arquivo)



config = carregar_config()

filtros = config["filtros"]


VALOR_MAXIMO = filtros["valor_maximo"]

CIDADE = filtros["cidade"]

TIPO = filtros["tipo"]

FINALIDADE = filtros["finalidade"]



def aprovado(imovel):

    texto = (
        str(imovel.get("titulo", ""))
        + " "
        + str(imovel.get("localizacao", ""))
        + " "
        + str(imovel.get("valor", ""))
    ).lower()


    # Cidade
    if CIDADE.lower() not in texto:
        return False


    # Tipo
    if TIPO.lower() not in texto:
        return False


    # Finalidade
    if FINALIDADE.lower() not in texto:
        return False


    # Valor
    valor = str(imovel.get("valor", ""))

    numeros = (
        valor
        .replace("R$", "")
        .replace(".", "")
        .replace(",", ".")
    )

    import re

    encontrado = re.search(
        r"\d+(\.\d+)?",
        numeros
    )

    if not encontrado:
        return False


    valor_numero = float(encontrado.group())


    if valor_numero > VALOR_MAXIMO:
        return False


    return True



    # Verifica tipo

    if TIPO.lower() not in texto:
        return False



    # Verifica finalidade

    if FINALIDADE.lower() not in texto:
        return False



    # Verifica valor

    valor_limpo = (
        valor
        .replace("R$", "")
        .replace(".", "")
        .replace(",", ".")
    )


    try:

        valor_numero = float(valor_limpo)

    except:

        return False



    if valor_numero > VALOR_MAXIMO:
        return False



    return True