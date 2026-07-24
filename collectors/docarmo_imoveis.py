from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


class ColetorDoCarmoImoveis:

    def __init__(self):
        self.origem = "Do Carmo Imóveis"
        self.url = "https://www.docarmoimoveis.com.br/aluguel/?&pagina=1"


    def coletar(self):

        print(f"[{self.origem}] Iniciando coleta")

        imoveis = []

        with sync_playwright() as p:

            navegador = p.chromium.launch(headless=True)

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

                print(f"[{self.origem}] Erro ao acessar página:", e)
                navegador.close()
                return imoveis


            navegador.close()


        soup = BeautifulSoup(html, "lxml")

        cards = soup.select("div.card.card_imovel_style")

        print(f"[{self.origem}] Cards encontrados: {len(cards)}")


        for card in cards:

            try:

                # O link fica no elemento pai <a>
                link = ""

                if card.parent.name == "a":
                    link = card.parent.get("href", "")


                imagem = ""

                img = card.select_one("img.img-imovel")

                if img:
                    imagem = img.get("src", "")


                codigo = ""

                if img:
                    codigo = img.get("data-codimovel", "")


                titulo = ""

                titulo_tag = card.select_one("h2.card-title")

                if titulo_tag:
                    titulo = titulo_tag.get_text(
                        " ",
                        strip=True
                    )


                localizacao = ""

                local_tag = card.select_one(
                    "span.card-text"
                )

                if local_tag:
                    localizacao = local_tag.get_text(
                        " ",
                        strip=True
                    )


                valor = ""

                valor_tag = card.select_one(
                    "strong.preco-imovel-card"
                )

                if valor_tag:
                    valor = valor_tag.get_text(
                        " ",
                        strip=True
                    )


                # Dados dos ícones
                quartos = ""
                vagas = ""
                area = ""


                icones = card.select(
                    ".container-icon"
                )


                for item in icones:

                    texto = item.get_text(
                        " ",
                        strip=True
                    )


                    if "m²" in texto:
                        area = texto.replace(
                            "m²",
                            ""
                        ).strip()


                    elif "Quarto" in texto:
                        partes = texto.split()

                        if partes:
                            quartos = partes[0]


                    elif "Vaga" in texto:
                        partes = texto.split()

                        if partes:
                            vagas = partes[0]


                imoveis.append({

                    "origem": self.origem,
                    "codigo": codigo,
                    "titulo": titulo,
                    "localizacao": localizacao,
                    "valor": valor,
                    "quartos": quartos,
                    "vagas": vagas,
                    "area": area,
                    "imagem": imagem,
                    "link": link

                })


            except Exception as e:

                print(
                    f"[{self.origem}] Erro lendo imóvel:",
                    e
                )


        return imoveis