import sqlite3
from pathlib import Path
from datetime import datetime


# Caminho do banco
CAMINHO_BANCO = Path("database/monitor.db")


def conectar():

    CAMINHO_BANCO.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(CAMINHO_BANCO)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS imoveis (

            origem TEXT NOT NULL,
            codigo TEXT NOT NULL,
            titulo TEXT,
            localizacao TEXT,
            valor TEXT,
            quartos TEXT,
            vagas TEXT,
            area TEXT,
            imagem TEXT,
            link TEXT,
            data_cadastro TEXT,
            tipo_negocio TEXT,
            tipo_imovel TEXT,
            suites TEXT,

            PRIMARY KEY (origem, codigo)

        )
    """)


    conn.execute("""
        CREATE TABLE IF NOT EXISTS status_monitor (

            id INTEGER PRIMARY KEY,
            status TEXT,
            mensagem TEXT,
            inicio TEXT,
            fim TEXT

        )
    """)


    conn.execute("""
        CREATE TABLE IF NOT EXISTS execucoes (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_execucao TEXT,
            coletados INTEGER,
            aprovados INTEGER,
            novos INTEGER

        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS monitor_config (

            id INTEGER PRIMARY KEY CHECK (id = 1),

            email TEXT,

            cidade TEXT,
            finalidade TEXT,
            tipo TEXT,
            bairro TEXT,
            valor_maximo REAL,
            quartos INTEGER,
            vagas INTEGER,
            imobiliaria TEXT,

            ativo INTEGER DEFAULT 0,

            data_cadastro TEXT

        )
        """)

    conn.execute("""
        INSERT OR IGNORE INTO monitor_config(id, ativo)
        VALUES (1, 0)
        """)

    conn.commit()

    return conn


def ja_existe(origem, codigo):

    conn = conectar()

    resultado = conn.execute("""
        SELECT 1
        FROM imoveis
        WHERE origem = ?
        AND codigo = ?
    """, (
        origem,
        codigo
    )).fetchone()

    conn.close()

    return resultado is not None



def salvar(imovel):

    conn = conectar()

    data_atual = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )


    conn.execute("""
        INSERT OR REPLACE INTO imoveis (

            origem,
            codigo,
            titulo,
            localizacao,
            valor,
            quartos,
            vagas,
            area,
            imagem,
            link,
            data_cadastro,
            tipo_negocio,
            tipo_imovel,
            suites

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        imovel.get("origem", ""),
        imovel.get("codigo", ""),
        imovel.get("titulo", ""),
        imovel.get("localizacao", ""),
        imovel.get("valor", ""),
        imovel.get("quartos", ""),
        imovel.get("vagas", ""),
        imovel.get("area", ""),
        imovel.get("imagem", ""),
        imovel.get("link", ""),
        data_atual,
        imovel.get("tipo_negocio", ""),
        imovel.get("tipo_imovel", ""),
        imovel.get("suites", ""),

    ))


    conn.commit()
    conn.close()



def iniciar_status():

    conn = conectar()

    data = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )


    conn.execute("""
        DELETE FROM status_monitor
    """)


    conn.execute("""
        INSERT INTO status_monitor (

            id,
            status,
            mensagem,
            inicio,
            fim

        )

        VALUES (?, ?, ?, ?, ?)

    """, (

        1,
        "Executando",
        "Iniciando monitor...",
        data,
        ""

    ))


    conn.commit()
    conn.close()



def atualizar_status(mensagem):

    conn = conectar()


    conn.execute("""
        UPDATE status_monitor

        SET mensagem = ?

        WHERE id = 1

    """, (
        mensagem,
    ))


    conn.commit()
    conn.close()



def finalizar_status():

    conn = conectar()

    data = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )


    conn.execute("""
        UPDATE status_monitor

        SET

            status = ?,
            mensagem = ?,
            fim = ?

        WHERE id = 1

    """, (

        "Finalizado",
        "Monitor concluído com sucesso.",
        data

    ))


    conn.commit()
    conn.close()



def salvar_execucao(
    total_coletados,
    total_aprovados,
    total_novos
):

    conn = conectar()

    data_atual = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )


    conn.execute("""
        INSERT INTO execucoes (

            data_execucao,
            coletados,
            aprovados,
            novos

        )

        VALUES (?, ?, ?, ?)

    """, (

        data_atual,
        total_coletados,
        total_aprovados,
        total_novos

    ))


    conn.commit()
    conn.close()

def salvar_monitor_config(config):

    conn = conectar()

    data_atual = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    conn.execute("""
        UPDATE monitor_config

        SET
            email = ?,
            cidade = ?,
            finalidade = ?,
            tipo = ?,
            bairro = ?,
            valor_maximo = ?,
            quartos = ?,
            vagas = ?,
            imobiliaria = ?,
            ativo = 1,
            data_cadastro = ?

        WHERE id = 1
    """, (

        config.get("email", ""),
        config.get("cidade", ""),
        config.get("finalidade", ""),
        config.get("tipo", ""),
        config.get("bairro", ""),
        config.get("valor_maximo", ""),
        config.get("quartos", ""),
        config.get("vagas", ""),
        config.get("imobiliaria", ""),
        data_atual

    ))

    conn.commit()
    conn.close()

def carregar_monitor_config():

    conn = conectar()

    resultado = conn.execute("""
        SELECT

            email,
            cidade,
            finalidade,
            tipo,
            bairro,
            valor_maximo,
            quartos,
            vagas,
            imobiliaria,
            ativo

        FROM monitor_config

        WHERE id = 1

    """).fetchone()

    conn.close()

    if not resultado:

        return {}

    return {

        "email": resultado[0],
        "cidade": resultado[1],
        "finalidade": resultado[2],
        "tipo": resultado[3],
        "bairro": resultado[4],
        "valor_maximo": resultado[5],
        "quartos": resultado[6],
        "vagas": resultado[7],
        "imobiliaria": resultado[8],
        "ativo": bool(resultado[9])

    }


    return {}