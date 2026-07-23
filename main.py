from collectors.seguranca_imoveis import ColetorSegurancaImoveis
from collectors.seguranca_aluguel import ColetorSegurancaAluguel
from app.filtros import aprovado
from app.notificacao import enviar_email
from database.banco import ja_existe, salvar


def main():

    print("=" * 50)
    print("MonitorImoveisGV")
    print("=" * 50)

    imoveis = []

    # Coletor de imóveis de venda
    coletor_venda = ColetorSegurancaImoveis()
    imoveis.extend(coletor_venda.coletar())

    # Coletor de imóveis de aluguel
    coletor_aluguel = ColetorSegurancaAluguel()
    imoveis.extend(coletor_aluguel.coletar())

    # Aplica os filtros
    aprovados = []

    for imovel in imoveis:
        if aprovado(imovel):
            aprovados.append(imovel)

    print()
    print(f"Imóveis coletados: {len(imoveis)}")
    print(f"Imóveis aprovados pelos filtros: {len(aprovados)}")

    # Verifica quais imóveis ainda não foram enviados
    novos = []

    for imovel in aprovados:
        if not ja_existe(imovel["codigo"]):
            novos.append(imovel)

    if novos:

        print()
        print(f"Novos imóveis encontrados: {len(novos)}")

        for imovel in novos:

            print()
            print("--------------------------------")
            print(imovel["titulo"])
            print(imovel["valor"])
            print(imovel["link"])

        # Envia o e-mail
        enviar_email(novos)

        # Salva somente após o envio
        for imovel in novos:
            salvar(imovel)

    else:
        print()
        print("Nenhum imóvel novo encontrado.")

    print()
    print("Processo finalizado.")


if __name__ == "__main__":
    main()