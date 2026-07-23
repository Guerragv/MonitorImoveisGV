import sqlite3

conn = sqlite3.connect("database/monitor.db")

cursor = conn.cursor()

cursor.execute("""
SELECT
    origem,
    codigo,
    titulo,
    valor,
    quartos,
    suites,
    vagas,
    area
FROM imoveis
ORDER BY id DESC
""")

dados = cursor.fetchall()

print(f"\nEncontrados {len(dados)} imóveis\n")

for linha in dados:
    print("-" * 60)
    print(linha)

conn.close()