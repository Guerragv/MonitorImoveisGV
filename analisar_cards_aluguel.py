from bs4 import BeautifulSoup

with open("pagina_aluguel_debug.html", "r", encoding="utf-8") as arquivo:
    html = arquivo.read()

soup = BeautifulSoup(html, "html.parser")

for tag in soup.find_all("div", class_=True):
    classes = " ".join(tag.get("class"))

    if "property" in classes.lower() or "imovel" in classes.lower():
        print(classes)