from bs4 import BeautifulSoup

with open("pagina_centro.html", "r", encoding="utf-8") as arquivo:
    html = arquivo.read()

soup = BeautifulSoup(html, "html.parser")


elementos = soup.find_all(string=lambda texto: texto and "Cód.:" in texto)

print("Encontrados:", len(elementos))

for i, item in enumerate(elementos[:3]):

    print("\n======================")
    print("IMÓVEL", i + 1)

    elemento = item.parent

    for nivel in range(5):
        elemento = elemento.parent

        print("\nNÍVEL", nivel + 1)
        print(elemento.name, elemento.get("class"))

        texto = elemento.get_text(" ", strip=True)

        print(texto[:500])