from collectors.seguranca_imoveis import ColetorSegurancaImoveis


coletor = ColetorSegurancaImoveis()

resultado = coletor.coletar()


for imovel in resultado:

    print("----------------")
    print(imovel)