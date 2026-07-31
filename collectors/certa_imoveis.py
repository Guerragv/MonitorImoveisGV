import requests
from bs4 import BeautifulSoup

from app.classificador import (
    identificar_tipo_imovel,
    identificar_negocio,
)


class ColetorCertaImoveis:

    def __init__(self):

        self.origem = "Certa Imóveis"

        self.url = (
            "https://www.certaimoveis.com.br/imoveis/aluguel"
        )


    def coletar(self):

        print(
            f"[{self.origem}] Iniciando coleta"
        )


        headers = {
            "User-Agent": "Mozilla/5.0"
        }


        try:

            resposta = requests.get(
                self.url,
                headers=headers,
                timeout=30
            )

            resposta.raise_for_status()


        except Exception as erro:

            print(
                f"[{self.origem}] Erro ao acessar site:",
                erro
            )

            return []



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
            f"[{self.origem}] Cards encontrados: {len(cards)}"
        )



        for card in cards:

            try:


                # ==========================
                # CÓDIGO
                # ==========================

                codigo_tag = card.find(
                    "input",
                    class_="onAddFavorito"
                )


                if not codigo_tag:
                    continue


                codigo = codigo_tag.get(
                    "value",
                    ""
                )



                # ==========================
                # TÍTULO
                # ==========================

                titulo = ""


                titulo_tag = card.find(
                    "p",
                    class_="tit"
                )


                if titulo_tag:

                    titulo = titulo_tag.get_text(
                        strip=True
                    )



                # ==========================
                # VALOR
                # ==========================

                valor = ""


                valor_tag = card.find(
                    "p",
                    class_="value"
                )


                if valor_tag:

                    valor = valor_tag.get_text(
                        " ",
                        strip=True
                    )



                # ==========================
                # ENDEREÇO
                # ==========================

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



                # ==========================
                # FILTRO CIDADE
                # ==========================

                if "governador valadares" not in endereco.lower():

                    continue



                # ==========================
                # IMAGEM
                # ==========================

                imagem = ""


                img = card.find(
                    "img",
                    class_="image"
                )


                if img:

                    imagem = img.get(
                        "src",
                        ""
                    )



                # ==========================
                # LINK
                # ==========================

                link = ""


                link_tag = card.find(
                    "a",
                    class_="abrir_link"
                )


                if link_tag:

                    link = link_tag.get(
                        "href",
                        ""
                    )



                # ==========================
                # INFORMAÇÕES
                # ==========================

                quartos = ""

                vagas = ""

                area = ""


                itens = card.select(
                    "ul.list_items li"
                )


                for item in itens:

                    texto_item = item.get_text(
                        " ",
                        strip=True
                    )


                    valor_item = item.find(
                        "b"
                    )


                    if not valor_item:

                        continue


                    numero = valor_item.get_text(
                        strip=True
                    )


                    if "Quarto" in texto_item:

                        quartos = numero


                    elif "Vaga" in texto_item:

                        vagas = numero


                    elif "Área" in texto_item:

                        area = numero



                # ==========================
                # MONTA IMÓVEL
                # ==========================

                imovel = {

                    "origem": self.origem,

                    "codigo": codigo,

                    "titulo": titulo,

                    "localizacao": endereco,

                    "valor": valor,

                    "quartos": quartos,

                    "vagas": vagas,

                    "area": area,

                    "imagem": imagem,

                    "link": link,


                    "tipo_negocio": identificar_negocio(
                        titulo
                    ),


                    "tipo_imovel": identificar_tipo_imovel(
                        titulo
                    ),

                }



                print(
                    "ADICIONANDO:",
                    codigo,
                    "|",
                    titulo,
                    "|",
                    valor
                )



                imoveis.append(
                    imovel
                )



            except Exception as erro:


                print(
                    "[Certa Imóveis] Erro lendo card:",
                    erro
                )



        print(
            "\n=== TODOS OS IMÓVEIS DA CERTA ==="
        )


        for imovel in imoveis:

            print(
                imovel["codigo"],
                "|",
                imovel["tipo_imovel"],
                "|",
                imovel["titulo"],
                "|",
                imovel["valor"]
            )



        return imoveis