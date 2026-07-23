from bs4 import BeautifulSoup

with open("pagina_centro.html", "r", encoding="utf-8") as arquivo:
    html = arquivo.read()

soup = BeautifulSoup(html, "html.parser")

card = soup.find("div", {"data-codigo": "14836"})

print("=== AMENITIES ===")

for item in card.select(".property-amenities"):
    print(item.prettify()[:2000])
    print("----------------")