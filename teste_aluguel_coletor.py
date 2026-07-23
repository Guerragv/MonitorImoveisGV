from collectors.seguranca_aluguel import ColetorSegurancaAluguel


coletor = ColetorSegurancaAluguel()

imoveis = coletor.coletar()


print()

for i in imoveis:
    print(i)