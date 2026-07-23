from bs4 import BeautifulSoup


with open(
    "pagina_aluguel_playwright.html",
    "r",
    encoding="utf-8"
) as f:
    html = f.read()


soup = BeautifulSoup(html, "lxml")


card = soup.select_one(".imovel-box-single")


print(card.prettify())