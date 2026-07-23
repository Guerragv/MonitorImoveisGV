from collectors.seguranca_aluguel import ColetorSegurancaAluguel


coletor = ColetorSegurancaAluguel()

resultado = coletor.coletar()


print()

for imovel in resultado:
    print(imovel)