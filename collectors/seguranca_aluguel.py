from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


class ColetorSegurancaAluguel:

    def coletar(self):

        print("[Segurança Aluguel] Iniciando coleta")

        url = "https://segurancaimoveisgv.com.br/aluguel/tipo/cidadebairro/?categoriagrupo=Residencial"

        imoveis = []

        with sync_playwright() as p:

            navegador = p.chromium.launch(headless=True)

            pagina = navegador.new_page()

            pagina.goto(
                url,
                wait_until="networkidle",
                timeout=60000
            )

            pagina.wait_for_selector(
                ".imovel-box-single",
                timeout=30000
            )

            html = pagina.content()

            navegador.close()


        soup = BeautifulSoup(html, "html.parser")


        cards = soup.select(".imovel-box-single")

        print(f"[Segurança Aluguel] Cards encontrados: {len(cards)}")


        for card in cards:

            try:

                codigo = card.get("data-codigo")

                titulo = card.select_one(
                    ".titulo-grid"
                ).text.strip()


                localizacao = card.select_one(
                    "h3"
                ).text.strip()


                valor = card.select_one(
                    ".item-price-rent"
                )

                if valor:
                    valor = valor.text.strip()
                else:
                    valor = ""


                link = card.select_one(
                    "a[href*='/imovel/']"
                )

                if link:
                    link = link["href"]
                else:
                    link = ""


                imoveis.append({

                    "origem": "Segurança Aluguel",
                    "codigo": codigo,
                    "titulo": titulo,
                    "localizacao": localizacao,
                    "valor": valor,
                    "link": link

                })


            except Exception as e:

                print(
                    "Erro lendo imóvel:",
                    e
                )


        return imoveis