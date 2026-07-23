import sqlite3


conexao = sqlite3.connect("database/monitor.db")

cursor = conexao.cursor()

cursor.execute("""
SELECT *
FROM imoveis
""")

dados = cursor.fetchall()

print(f"Total de imóveis no banco: {len(dados)}\n")

for item in dados:
    print(item)

conexao.close()