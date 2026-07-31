import re


def aprovado(imovel, filtros):


    tipo_imovel = str(
        imovel.get("tipo_imovel", "")
    ).strip().lower()


    tipo_negocio = str(
        imovel.get("tipo_negocio", "")
    ).strip().lower()



    # Tipo do imóvel
    if filtros.get("tipo"):

        if filtros["tipo"].lower() != tipo_imovel:

            return False



    # Finalidade
    if filtros.get("finalidade"):

        if filtros["finalidade"].lower() != tipo_negocio:

            return False



    # Valor máximo
    if filtros.get("valor_maximo"):


        valor = str(
            imovel.get("valor", "")
        )


        encontrado = re.search(
            r"\d[\d\.]*,\d{2}",
            valor
        )


        if encontrado:

            valor_limpo = (
                encontrado.group()
                .replace(".", "")
                .replace(",", ".")
            )


            valor_numero = float(
                valor_limpo
            )


            if valor_numero > float(
                filtros["valor_maximo"]
            ):

                return False



    return True