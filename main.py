from collectors.seguranca_imoveis import ColetorSegurancaImoveis
from collectors.seguranca_aluguel import ColetorSegurancaAluguel
from collectors.docarmo_imoveis import ColetorDoCarmoImoveis
from collectors.certa_imoveis import ColetorCertaImoveis
from collectors.perim_imoveis import ColetorPerimImoveis

from app.filtros import aprovado
from app.notificacao import enviar_email
from app.configuracao import carregar_config
from database.banco import ja_existe, salvar

from datetime import datetime
from pathlib import Path
import sys


# ==============================
# LOG
# ==============================

BASE_DIR = Path(__file__).resolve().parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

arquivo_log = LOG_DIR / f"monitor_{datetime.now().strftime('%Y-%m-%d')}.log"


class Logger:

    def __init__(self):
        self.terminal = sys.stdout
        self.arquivo = open(
            arquivo_log,
            "a",
            encoding="utf-8"
        )

    def write(self, mensagem):
        self.terminal.write(mensagem)
        self.arquivo.write(mensagem)
        self.arquivo.flush()

    def flush(self):
        pass


sys.stdout = Logger()



# ==============================
# PRINCIPAL
# ==============================

def main():

    print()
    print("=" * 50)
    print(
        "MonitorImoveisGV -",
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )
    print("=" * 50)


    config = carregar_config()

    sites = config["sites"]


    imoveis = []


    # ==============================
    # COLETORES
    # ==============================


    if sites["seguranca_imoveis"]:

        coletor_venda = ColetorSegurancaImoveis()

        imoveis.extend(
            coletor_venda.coletar()
        )



    if sites["seguranca_aluguel"]:

        coletor_aluguel = ColetorSegurancaAluguel()

        imoveis.extend(
            coletor_aluguel.coletar()
        )



    if sites["do_carmo"]:

        coletor_docarmo = ColetorDoCarmoImoveis()

        imoveis.extend(
            coletor_docarmo.coletar()
        )



    if sites["certa"]:

        coletor_certa = ColetorCertaImoveis()

        imoveis.extend(
            coletor_certa.coletar()
        )



    if sites["perim"]:

        coletor_perim = ColetorPerimImoveis()

        imoveis.extend(
            coletor_perim.coletar()
        )



    # ==============================
    # FILTROS
    # ==============================

    aprovados = []


    for imovel in imoveis:

        if aprovado(imovel):

            aprovados.append(imovel)



    print()

    print(
        f"Imóveis coletados: {len(imoveis)}"
    )

    print(
        f"Imóveis aprovados pelos filtros: {len(aprovados)}"
    )



    # ==============================
    # NOVOS IMÓVEIS
    # ==============================

    novos = []


    for imovel in aprovados:

        if not ja_existe(
            imovel["origem"],
            imovel["codigo"]
        ):

            novos.append(imovel)



    if novos:


        print()

        print(
            f"Novos imóveis encontrados: {len(novos)}"
        )



        for imovel in novos:

            print()

            print("-" * 40)

            print(
                "Origem:",
                imovel.get("origem")
            )

            print(
                "Código:",
                imovel.get("codigo")
            )

            print(
                "Título:",
                imovel.get("titulo")
            )

            print(
                "Valor:",
                imovel.get("valor")
            )

            print(
                "Local:",
                imovel.get("localizacao")
            )

            print(
                "Link:",
                imovel.get("link")
            )



        # Envia e salva

        for imovel in novos:


            enviado = enviar_email(imovel)


            if enviado:

                salvar(imovel)

                print(
                    "Imóvel salvo no banco."
                )


            else:

                print(
                    "Imóvel não salvo porque o e-mail falhou."
                )



    else:

        print()

        print(
            "Nenhum imóvel novo encontrado."
        )



    print()

    print(
        "Processo finalizado."
    )



if __name__ == "__main__":

    main()