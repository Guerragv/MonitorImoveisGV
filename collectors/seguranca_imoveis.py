import requests
from bs4 import BeautifulSoup


class ColetorSegurancaImoveis:

    URL = "https://segurancaimoveisgv.com.br/venda/residencial/governador-valadares/centro/"

    def __init__(self):
        self.origem = "Segurança Imóveis"

    def coletar(self):
        print("[Segurança Imóveis] Iniciando coleta")

        resposta = requests.get(
            self.URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=30
        )

        resposta.raise_for_status()

        soup = BeautifulSoup(resposta.text, "html.parser")

        cards = soup.select("div.imovel-box-single")

        print(f"[Segurança Imóveis] Encontrados: {len(cards)} imóveis")

        imoveis = []

        for card in cards:

            codigo = card.get("data-codigo")

            # Título
            titulo = card.select_one("h2.titulo-grid")

            # Localização
            localizacao = card.select_one(
                "h3[itemprop='streetAddress']"
            )

            # Valor
            valor = card.select_one(
                ".thumb-price"
            )

            # Link
            link = None
            a = card.select_one("a[href]")

            if a:
                link = a.get("href")

            # Imagem
            imagem = None

            foto = card.select_one(
                ".foto-imovel"
            )

            if foto:

                estilo = foto.get(
                    "style",
                    ""
                )

                if "url(" in estilo:
                    try:
                        imagem = estilo.split("url(")[1]
                        imagem = imagem.replace('"', '')
                        imagem = imagem.replace(")", '')
                        imagem = imagem.strip()

                    except Exception:
                        imagem = None

            # Características
            quartos = None
            suites = None
            vagas = None
            area = None

            caracteristicas = card.select(
                ".amenities-main > div"
            )

            for item in caracteristicas:

                texto = item.get_text(
                    " ",
                    strip=True
                )

                if "Quartos" in texto:
                    quartos = (
                        texto
                        .replace("Quartos", "")
                        .strip()
                    )

                elif "Suíte" in texto:
                    suites = (
                        texto
                        .replace("Suíte", "")
                        .strip()
                    )

                elif "Vagas" in texto:
                    vagas = (
                        texto
                        .replace("Vagas", "")
                        .strip()
                    )

                elif "m²" in texto:
                    area = texto


            imovel = {
                "origem": self.origem,
                "codigo": codigo,
                "titulo": (
                    titulo.text.strip()
                    if titulo
                    else None
                ),
                "localizacao": (
                    localizacao.get_text(
                        " ",
                        strip=True
                    )
                    if localizacao
                    else None
                ),
                "valor": (
                    valor.text.strip()
                    if valor
                    else None
                ),
                "quartos": quartos,
                "suites": suites,
                "vagas": vagas,
                "area": area,
                "imagem": imagem,
                "link": link
            }

            imoveis.append(imovel)

        return imoveis