from database.banco import salvar, ja_existe

imovel = {
    "codigo": "12345",
    "titulo": "Casa Teste",
    "valor": "R$ 900",
    "link": "https://teste.com"
}

print("Existe antes:", ja_existe("12345"))

salvar(imovel)

print("Existe depois:", ja_existe("12345"))