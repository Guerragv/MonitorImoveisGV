from playwright.sync_api import sync_playwright

url = "https://segurancaimoveisgv.com.br/venda/residencial/governador-valadares/centro/"

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)

    pagina = navegador.new_page()

    pagina.goto(url, wait_until="networkidle")

    pagina.wait_for_timeout(8000)

    print("Título:")
    print(pagina.title())

    print("\nTexto da página:")
    texto = pagina.locator("body").inner_text()

    print(texto[:3000])

    with open("texto_centro.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)
    
    with open("pagina_centro.html", "w", encoding="utf-8") as arquivo:
        arquivo.write(pagina.content())

    navegador.close()