from collectors.seguranca_imoveis import ColetorSegurancaImoveis
from collectors.seguranca_aluguel import ColetorSegurancaAluguel
from collectors.docarmo_imoveis import ColetorDoCarmoImoveis
from collectors.certa_imoveis import ColetorCertaImoveis
from collectors.perim_imoveis import ColetorPerimImoveis


from app.filtros import aprovado
from app.notificacao import enviar_email
from app.configuracao import carregar_config
from app.logger import configurar_logger

from database.banco import (
    carregar_monitor_config,
    ja_existe,
    salvar,
    salvar_execucao,
    iniciar_status,
    finalizar_status
)

from database.backup import criar_backup

from datetime import datetime
from pathlib import Path
import sys

logger = configurar_logger()

logger.info(
    "Monitor iniciado"
)

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
        self.terminal.flush()


sys.stdout = Logger()

def main():

    filtros = carregar_monitor_config()

    print("FILTRO ATUAL DO MONITOR:")
    print(filtros)

    iniciar_status()

    print()
    print("=" * 50)
    print(
        "MonitorImoveisGV -",
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )
    print("=" * 50)


    # Cria backup do banco antes da execução
    criar_backup()


    # Carrega configurações
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

        print(
            imovel.get("origem"),
            "|",
            imovel.get("titulo"),
            "|",
            imovel.get("tipo_imovel"),
            "|",
            imovel.get("tipo_negocio"),
            "|",
            imovel.get("valor")
        )


        if aprovado(imovel, filtros):

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


    for imovel in imoveis:

        if aprovado(imovel, filtros):

            if not ja_existe(
                imovel["origem"],
                imovel["codigo"]
            ):

                salvar(imovel)

                novos.append(imovel)


                print(
                    f"Imóvel aprovado salvo: {imovel['origem']} | {imovel['codigo']}"
                )



    print()


    print(
        f"Novos imóveis encontrados: {len(novos)}"
    )



    # Exibe imóveis novos

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
    # ==============================
    # ENVIO DE EMAIL
    # ==============================

    for imovel in novos:

        enviado = enviar_email(imovel)


        if not enviado:

            print(
                "Falha no envio do e-mail."
            )



    # ==============================
    # REGISTRA EXECUÇÃO
    # ==============================

    salvar_execucao(
        len(imoveis),
        len(aprovados),
        len(novos)
    )


    finalizar_status()


    print()


    logger.info(
        "Processo finalizado"
    )


    print(
        "Processo finalizado."
    )



if __name__ == "__main__":

    main()