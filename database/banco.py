import sqlite3
from pathlib import Path

# Caminho do banco
CAMINHO_BANCO = Path("data/imoveis.db")


def conectar():
    CAMINHO_BANCO.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS imoveis (
            codigo TEXT PRIMARY KEY,
            titulo TEXT,
            valor TEXT,
            link TEXT
        )
    """)
    conn.commit()

    return conn


def ja_existe(codigo):
    conn = conectar()

    cursor = conn.execute(
        "SELECT codigo FROM imoveis WHERE codigo=?",
        (codigo,)
    )

    resultado = cursor.fetchone()

    conn.close()

    return resultado is not None


def salvar(imovel):
    conn = conectar()

    conn.execute("""
        INSERT OR IGNORE INTO imoveis
        (codigo, titulo, valor, link)
        VALUES (?, ?, ?, ?)
    """, (
        imovel["codigo"],
        imovel["titulo"],
        imovel["valor"],
        imovel["link"]
    ))

    conn.commit()
    conn.close()