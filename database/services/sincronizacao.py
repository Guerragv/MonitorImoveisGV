from database.consultas import buscar_imovel
from database.banco import salvar_imovel


def sincronizar(lista_imoveis):
    """
    Sincroniza os imóveis coletados com o banco.
    """

    novos = 0
    atualizados = 0

    for imovel in lista_imoveis:

        existente = buscar_imovel(
            imovel["origem"],
            imovel["codigo"]
        )

        if existente is None:

            salvar_imovel(imovel)
            novos += 1

        else:

            salvar_imovel(imovel)
            atualizados += 1

    print()
    print("=" * 40)
    print("Resumo da sincronização")
    print("=" * 40)
    print(f"Novos: {novos}")
    print(f"Atualizados: {atualizados}")