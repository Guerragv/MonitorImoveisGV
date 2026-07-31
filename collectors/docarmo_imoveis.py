from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from app.classificador import identificar_tipo_imovel, identificar_negocio


class ColetorDoCarmoImoveis:

    def __init__(self):
        self.origem = "Do Carmo Imóveis"
        self.url = "https://www.docarmoimoveis.com.br/aluguel/?&pagina=1"


    def coletar(self):

        print(f"[{self.origem}] Iniciando coleta")

        imoveis = []

        with sync_playwright() as p:

            navegador = p.chromium.launch(
                headless=True
            )

            pagina = navegador.new_page()


            try:

                pagina.goto(
                    self.url,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                pagina.wait_for_timeout(3000)

                html = pagina.content()


            except Exception as e:

                print(
                    f"[{self.origem}] Erro:",
                    e
                )

                navegador.close()

                return imoveis


            navegador.close()



        soup = BeautifulSoup(
            html,
            "lxml"
        )


        cards = soup.select(
            "a[href*='/imovel/']"
        )


        print(
            f"[{self.origem}] Cards encontrados: {len(cards)}"
        )



        for card in cards:

            try:

                link = card.get(
                    "href",
                    ""
                )


                codigo = ""


                img = card.select_one(
                    "img[data-codimovel]"
                )


                if img:

                    codigo = img.get(
                        "data-codimovel",
                        ""
                    )


                if not codigo:

                    continue



                imagem = ""


                if img:

                    imagem = img.get(
                        "src",
                        ""
                    )



                texto = card.get_text(
                    " ",
                    strip=True
                )



                titulo = ""


                titulo_tag = card.find(
                    "h2"
                )


                if titulo_tag:

                    titulo = titulo_tag.get_text(
                        " ",
                        strip=True
                    )


                else:

                    titulo = texto[:100]



                valor = ""


                if "R$" in texto:

                    partes = texto.split("R$")


                    if len(partes) > 1:

                        valor = (
                            "R$ "
                            + partes[1].split()[0]
                        )



                localizacao = ""


                if " no " in titulo.lower():

                    localizacao = (
                        titulo.lower()
                        .split(" no ")[-1]
                    )

                    localizacao = localizacao.title()



                imovel = {

                    "origem": self.origem,

                    "codigo": codigo,

                    "titulo": titulo,

                    "localizacao": localizacao,

                    "valor": valor,

                    "quartos": "",

                    "vagas": "",

                    "area": "",

                    "imagem": imagem,

                    "link": link,

                    "tipo_negocio": identificar_negocio(titulo),

                    "tipo_imovel": identificar_tipo_imovel(titulo),

                }


                imoveis.append(
                    imovel
                )



            except Exception as e:

                print(
                    f"[{self.origem}] Erro lendo imóvel:",
                    e
                )



        return imoveis