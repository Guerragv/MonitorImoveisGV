import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def enviar_email(imoveis):

    if not imoveis:
        print("Nenhum imóvel para enviar.")
        return


    # Configurações do e-mail
    remetente = "monitorimoveisgv@gmail.com"
    senha = "jsxy ctmu ayeh vpqr"
    destinatario = "guerragv83@gmail.com"


    assunto = "🏠 MonitorImoveisGV - Novo imóvel encontrado"


    corpo = """
Olá!

O MonitorImoveisGV encontrou novos imóveis dentro dos filtros configurados.

"""


    for imovel in imoveis:

        corpo += f"""
--------------------------------

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

"""


    corpo += """
--------------------------------

Este alerta foi enviado automaticamente pelo MonitorImoveisGV.
"""


    mensagem = MIMEMultipart()

    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto

    mensagem.attach(
        MIMEText(corpo, "plain", "utf-8")
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

        servidor.sendmail(
            remetente,
            destinatario,
            mensagem.as_string()
        )

        servidor.quit()


        print("E-mail enviado com sucesso!")


    except Exception as erro:

        print("Erro ao enviar e-mail:")
        print(erro)