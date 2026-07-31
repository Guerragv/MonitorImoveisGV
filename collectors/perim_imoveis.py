import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.perimimoveis.com.br/"

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

            imagem = ""

            img = pai.find("img")

            if img:

                imagem = (
                    img.get("src")
                    or img.get("data-src")
                    or img.get("data-original")
                    or ""
                )


            if imagem and not imagem.startswith("http"):

                imagem = BASE_URL + imagem.lstrip("/")

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

            suites = self.extrair(
                texto,
                r"Suítes\s+(\d+)"
            )

            vagas = self.extrair(
                texto,
                r"Garagem\s+(\d+)"
            )

            if not vagas:
                vagas = "0"


            bairro = ""

            padrao_bairro = r"R\$ ?[\d\.,]+\s+(.+?)\s+Casa"

            resultado = re.search(
                padrao_bairro,
                texto
            )           
            
            if resultado:
                bairro = resultado.group(1).strip()


            if href.startswith("http"):
                url_imovel = href
            else:
                url_imovel = BASE_URL + href.replace("../", "")

            titulo = "Casa"

            if quartos:
                titulo += f" {quartos} quarto"

                if quartos != "1":
                     titulo += "s"

            if bairro:
                titulo += f" - {bairro.title()}"


            imovel = {
                "origem": "Perim Imóveis",
                "codigo": codigo,
                "titulo": titulo,
                "localizacao": bairro.title(),
                "valor": valor,
                "quartos": quartos,
                "suites": suites,
                "vagas": vagas,
                "area": "",
                "imagem": imagem,
                "link": url_imovel,
                "tipo_negocio": "Aluguel",
                "tipo_imovel": "Casa",
            }
            

            imoveis.append(imovel)


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