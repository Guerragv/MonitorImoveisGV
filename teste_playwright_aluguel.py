from playwright.sync_api import sync_playwright


URL = "https://segurancaimoveisgv.com.br/aluguel/tipo/cidadebairro/?categoriagrupo=Residencial"


with sync_playwright() as p:

    navegador = p.chromium.launch(
        headless=False
    )

    pagina = navegador.new_page()

    print("Abrindo página...")

    pagina.goto(
        URL,
        wait_until="networkidle",
        timeout=60000
    )

    print("Título:")
    print(pagina.title())

    pagina.wait_for_timeout(5000)

    cards = pagina.locator(
        ".imovel-box-single"
    )

    print(
        "Cards encontrados:",
        cards.count()
    )


    html = pagina.content()

    with open(
        "pagina_aluguel_playwright.html",
        "w",
        encoding="utf-8"
    ) as arquivo:
        arquivo.write(html)


    navegador.close()