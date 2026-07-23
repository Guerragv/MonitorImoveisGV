from bs4 import BeautifulSoup

with open("pagina_centro.html", "r", encoding="utf-8") as arquivo:
    html = arquivo.read()

soup = BeautifulSoup(html, "html.parser")

card = soup.select_one(".imovel-box-single")

print(card.prettify()[:5000])