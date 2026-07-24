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
            PRIMARY KEY (origem, codigo)
        )
    """)

    # Garante que bancos antigos recebam a nova coluna
    colunas = [
        coluna[1]
        for coluna in conn.execute("PRAGMA table_info(imoveis)")
    ]

    if "data_cadastro" not in colunas:
        conn.execute("""
            ALTER TABLE imoveis
            ADD COLUMN data_cadastro TEXT
        """)

    conn.commit()

    return conn


def ja_existe(origem, codigo):
    conn = conectar()

    cursor = conn.execute("""
        SELECT 1
        FROM imoveis
        WHERE origem = ?
        AND codigo = ?
    """, (origem, codigo))

    resultado = cursor.fetchone()

    conn.close()

    return resultado is not None


def salvar(imovel):
    conn = conectar()

    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    conn.execute("""
        INSERT OR IGNORE INTO imoveis (
            codigo,
            origem,
            titulo,
            localizacao,
            valor,
            quartos,
            vagas,
            area,
            imagem,
            link,
            data_cadastro
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        imovel["codigo"],
        imovel.get("origem", ""),
        imovel.get("titulo", ""),
        imovel.get("localizacao", ""),
        imovel.get("valor", ""),
        imovel.get("quartos", ""),
        imovel.get("vagas", ""),
        imovel.get("area", ""),
        imovel.get("imagem", ""),
        imovel.get("link", ""),
        data_atual
    ))

    conn.commit()
    conn.close()