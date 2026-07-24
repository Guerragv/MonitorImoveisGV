import requests
from bs4 import BeautifulSoup


class ColetorCertaImoveis:

    def __init__(self):
        self.url = "https://www.certaimoveis.com.br/imoveis/aluguel"


    def coletar(self):

        print("[Certa Imóveis] Iniciando coleta")

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        resposta = requests.get(
            self.url,
            headers=headers
        )

        soup = BeautifulSoup(
            resposta.text,
            "html.parser"
        )


        imoveis = []

        cards = soup.find_all(
            "div",
            class_="div_imovel"
        )


        print(
            f"[Certa Imóveis] Cards encontrados: {len(cards)}"
        )


        for card in cards:

            try:

                # Código
                codigo = card.find(
                    "input",
                    class_="onAddFavorito"
                ).get("value")


                # Título
                titulo = card.find(
                    "p",
                    class_="tit"
                ).get_text(
                    strip=True
                )


                # Valor
                valor = card.find(
                    "p",
                    class_="value"
                ).get_text(
                    " ",
                    strip=True
                )


                # Endereço correto
                endereco = ""

                enderecos = card.find_all(
                    "div",
                    class_="address"
                )

                for item in enderecos:

                    texto_endereco = item.get_text(
                        " ",
                        strip=True
                    )

                    if (
                        texto_endereco
                        and
                        "Imóvel com" not in texto_endereco
                    ):
                        endereco = texto_endereco
                        break


                # Imagem
                imagem = card.find(
                    "img",
                    class_="image"
                ).get("src")


                # Link
                link = card.find(
                    "a",
                    class_="abrir_link"
                ).get("href")


                # Informações adicionais
                vagas = ""
                area = ""
                quartos = ""


                itens = card.select(
                    "ul.list_items li"
                )

                for item in itens:

                    texto_item = item.get_text(
                        " ",
                        strip=True
                    )


                    if "Vaga(s)" in texto_item:

                        vagas = item.find(
                            "b"
                        ).get_text(
                            strip=True
                        )


                    elif "Área" in texto_item:

                        area = item.find(
                            "b"
                        ).get_text(
                            strip=True
                        )


                # Quartos pelo link
                if "quartos" in link:

                    partes = link.split(
                        "-quartos"
                    )

                    trecho = partes[0]

                    numeros = trecho.split("-")

                    for numero in reversed(numeros):

                        if numero.isdigit():

                            quartos = numero
                            break


                imovel = {

                    "origem": "Certa Imóveis",
                    "codigo": codigo,
                    "titulo": titulo,
                    "localizacao": endereco,
                    "valor": valor,
                    "quartos": quartos,
                    "vagas": vagas,
                    "area": area,
                    "imagem": imagem,
                    "link": link

                }


                imoveis.append(imovel)


            except Exception as erro:

                print(
                    "[Certa Imóveis] Erro:",
                    erro
                )


        return imoveis