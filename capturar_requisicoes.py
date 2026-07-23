from playwright.sync_api import sync_playwright


url = "https://segurancaimoveisgv.com.br/imoveis/venda"


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    print("Abrindo página...")

    def capturar(request):
        if any(x in request.url.lower() for x in [
            "imovel",
            "api",
            "ajax",
            "busca",
            "filtro",
            "json"
        ]):
            print("\nREQUISIÇÃO:")
            print(request.url)

    page.on(
        "request",
        capturar
    )


    page.goto(
        url,
        wait_until="networkidle",
        timeout=60000
    )


    page.wait_for_timeout(10000)

    browser.close()