from collectors.imoveis_teste import ColetorImoveisTeste

coletor = ColetorImoveisTeste()

resultado = coletor.coletar()

print("\nImóveis encontrados:")
for imovel in resultado:
    print(imovel)