import smtplib
import yaml
from pathlib import Path

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def carregar_config():

    caminho = Path("config/config.yaml")

    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return yaml.safe_load(arquivo)



def enviar_email(imovel):

    config = carregar_config()

    email_config = config["notificacao"]

    remetente = email_config["remetente"]

    senha = email_config["senha_app"]

    destinatarios = email_config["destinatarios"]


    assunto = "🏠 MonitorImoveisGV - Novo imóvel encontrado"


    corpo = f"""
Olá!

O MonitorImoveisGV encontrou um novo imóvel dentro dos filtros configurados.

--------------------------------

Origem:
{imovel.get('origem', '')}

Código:
{imovel.get('codigo', '')}

Título:
{imovel.get('titulo', '')}

Valor:
{imovel.get('valor', '')}

Localização:
{imovel.get('localizacao', '')}

Quartos:
{imovel.get('quartos', '')}

Vagas:
{imovel.get('vagas', '')}

Área:
{imovel.get('area', '')}

Link:
{imovel.get('link', '')}

--------------------------------

Este alerta foi enviado automaticamente pelo MonitorImoveisGV.
"""


    mensagem = MIMEMultipart()

    mensagem["From"] = remetente

    mensagem["To"] = ", ".join(destinatarios)

    mensagem["Subject"] = assunto


    mensagem.attach(
        MIMEText(
            corpo,
            "plain",
            "utf-8"
        )
    )


    try:

        servidor = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        servidor.starttls()


        servidor.login(
            remetente,
            senha
        )


        servidor.send_message(
            mensagem,
            from_addr=remetente,
            to_addrs=destinatarios
        )


        servidor.quit()


        print("E-mail enviado com sucesso!")

        return True


    except Exception as erro:

        print("Erro ao enviar e-mail:")
        print(erro)

        return False