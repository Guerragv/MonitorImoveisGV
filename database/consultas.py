import sqlite3

DB = "database/monitor.db"


def conectar():
    return sqlite3.connect(DB)


def buscar_imovel(origem, codigo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM imoveis
        WHERE origem = ?
        AND codigo = ?
    """, (origem, codigo))

    resultado = cursor.fetchone()

    conn.close()

    return resultado


def listar_imoveis():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM imoveis
        ORDER BY origem, codigo
    """)

    resultado = cursor.fetchall()

    conn.close()

    return resultado


def contar_imoveis():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM imoveis
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total