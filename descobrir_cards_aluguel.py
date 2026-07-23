from playwright.sync_api import sync_playwright

URL = "https://segurancaimoveisgv.com.br/aluguel/tipo/cidadebairro/?categoriagrupo=Residencial"


with sync_playwright() as p:

    navegador = p.chromium.launch(headless=False)

    pagina = navegador.new_page()

    print("Abrindo página...")
    
    pagina.goto(URL, timeout=60000)

    pagina.wait_for_timeout(5000)

    html = pagina.content()

    with open("pagina_aluguel_debug.html", "w", encoding="utf-8") as arquivo:
        arquivo.write(html)

    print("HTML salvo")

    elementos = pagina.locator("a").count()

    print("Quantidade de links:", elementos)

    navegador.close()