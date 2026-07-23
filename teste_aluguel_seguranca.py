import requests
from bs4 import BeautifulSoup

url = "https://segurancaimoveisgv.com.br/aluguel/tipo/cidadebairro/?categoriagrupo=Residencial"

print("Acessando:")
print(url)

resposta = requests.get(url)

print("Status:", resposta.status_code)

soup = BeautifulSoup(resposta.text, "html.parser")

titulo = soup.title

print("Título:")
print(titulo.text if titulo else "Sem título")

print("\nQuantidade de caracteres HTML:")
print(len(resposta.text))

if "imovel" in resposta.text.lower():
    print("\nEncontrou referência a imóveis")
else:
    print("\nNão encontrou imóveis")