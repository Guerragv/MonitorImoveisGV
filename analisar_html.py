from bs4 import BeautifulSoup

with open("pagina_seguranca.html", "r", encoding="utf-8") as arquivo:
    html = arquivo.read()

soup = BeautifulSoup(html, "html.parser")

print("=== SCRIPTS ===")

for script in soup.find_all("script"):
    src = script.get("src")
    if src:
        print(src)