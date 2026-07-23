from playwright.sync_api import sync_playwright
from collectors.base import ColetorBase


class ColetorImoveisTeste(ColetorBase):

    def __init__(self):
        super().__init__("Imóveis Teste")

    def coletar(self):

        self.informar("Iniciando coleta")

        imoveis = []

        with sync_playwright() as p:

            navegador = p.chromium.launch(headless=False)

            pagina = navegador.new_page()

            pagina.goto("https://www.google.com")

            titulo = pagina.title()

            self.informar(f"Página acessada: {titulo}")

            imoveis.append({
                "titulo": "Imóvel teste",
                "preco": 300000,
                "cidade": "Governador Valadares",
                "link": "https://www.google.com"
            })

            navegador.close()

        return imoveis