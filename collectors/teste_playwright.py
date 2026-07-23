from playwright.sync_api import sync_playwright

print("Iniciando teste...")

with sync_playwright() as p:
    print("Playwright carregado")

    navegador = p.chromium.launch(headless=False)

    print("Navegador aberto")

    pagina = navegador.new_page()

    pagina.goto("https://www.google.com")

    print("Título:", pagina.title())

    navegador.close()

print("Fim do teste")