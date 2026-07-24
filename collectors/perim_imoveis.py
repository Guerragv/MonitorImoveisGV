import requests
from bs4 import BeautifulSoup
import re


class ColetorPerimImoveis:

    def __init__(self):

        self.origem = "Perim Imóveis"

        self.url_busca = (
            "https://www.perimimoveis.com.br/"
            "Busca_nova/tratar_busca.php"
        )

        self.url_lista = (
            "https://www.perimimoveis.com.br/"
            "listagem-de-imoveis.php?pagina=1"
        )


    def coletar(self):

        print("[Perim Imóveis] Iniciando coleta")

        session = requests.Session()


        dados = {

            "FINALIDADEIMOVEL": "1",
            "TIPOIMO": "1",
            "QUARTOS": "",
            "VALORMINIMO": "",
            "VALORMAXIMO": "1200",
            "CODIMOVEL": "",
            "buscar": "Buscar"

        }


        session.post(
            self.url_busca,
            data=dados
        )


        resposta = session.get(
            self.url_lista
        )


        soup = BeautifulSoup(
            resposta.text,
            "html.parser"
        )


        imoveis = []


        links = soup.find_all(
            "a",
            href=True
        )


        codigos = set()


        for link in links:

            href = link["href"]


            if "detalhes-imovel.php" not in href:
                continue


            codigo = re.search(
                r"imovel=(\d+)",
                href
            )


            if not codigo:
                continue


            codigo = codigo.group(1)


            if codigo in codigos:
                continue


            codigos.add(codigo)


            # procura o bloco do imóvel
            pai = link.find_parent()


            texto = pai.get_text(
                " ",
                strip=True
            )


            valor = self.extrair(
                texto,
                r"R\$ ?[\d\.,]+"
            )


            quartos = self.extrair(
                texto,
                r"Quartos\s+(\d+)"
            )


            vagas = self.extrair(
                texto,
                r"Garagem\s+(\d+)"
            )


            bairro = ""

            partes = texto.split()

            if "Casa" in partes:

                pos = partes.index("Casa")

                bairro = " ".join(
                    partes[max(0,pos-2):pos]
                )


            imoveis.append({

                "origem": self.origem,

                "codigo": codigo,

                "titulo": "Casa para aluguel",

                "localizacao": bairro,

                "valor": valor,

                "quartos": quartos,

                "vagas": vagas,

                "area": "",

                "imagem": "",

                "link":
                    "https://www.perimimoveis.com.br/"
                    + href.replace("../","")

            })


        print(
            f"[Perim Imóveis] Encontrados: {len(imoveis)} imóveis"
        )


        return imoveis



    def extrair(self, texto, regex):

        resultado = re.search(
            regex,
            texto
        )

        if resultado:

            if resultado.groups():

                return resultado.group(1)

            return resultado.group(0)


        return ""