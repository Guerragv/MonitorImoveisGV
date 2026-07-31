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


    assunto = (
        "🏠 MonitorImoveisGV - "
        "Novo imóvel encontrado"
    )


    corpo = f"""
    <html>
    <body>

    <h2>🏠 Novo imóvel encontrado</h2>

    <p>
    O MonitorImoveisGV encontrou um imóvel
    dentro dos filtros configurados.
    </p>


    <hr>


    <b>Origem:</b><br>
    {imovel.get('origem', '')}
    <br><br>


    <b>Código:</b><br>
    {imovel.get('codigo', '')}
    <br><br>


    <b>Título:</b><br>
    {imovel.get('titulo', '')}
    <br><br>


    <b>Valor:</b><br>
    {imovel.get('valor', '')}
    <br><br>


    <b>Localização:</b><br>
    {imovel.get('localizacao', '')}
    <br><br>


    <b>Quartos:</b><br>
    {imovel.get('quartos', '')}
    <br><br>


    <b>Vagas:</b><br>
    {imovel.get('vagas', '')}
    <br><br>


    <b>Área:</b><br>
    {imovel.get('area', '')}
    <br><br>


    <b>Link:</b><br>

    <a href="{imovel.get('link', '')}">
    Acessar imóvel
    </a>


    <hr>


    <small>
    Alerta automático enviado pelo MonitorImoveisGV.
    </small>


    </body>
    </html>
    """



    mensagem = MIMEMultipart(
        "alternative"
    )


    mensagem["From"] = remetente

    mensagem["To"] = ", ".join(
        destinatarios
    )

    mensagem["Subject"] = assunto



    mensagem.attach(
        MIMEText(
            corpo,
            "html",
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


        print(
            "E-mail enviado com sucesso!"
        )


        return True



    except Exception as erro:

        print(
            "Erro ao enviar e-mail:"
        )

        print(
            erro
        )


        return False