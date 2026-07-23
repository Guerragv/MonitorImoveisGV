import sqlite3
import os

print("Arquivos .db encontrados:")

for raiz, pastas, arquivos in os.walk("."):
    for arquivo in arquivos:
        if arquivo.endswith(".db"):
            print(os.path.join(raiz, arquivo))


print("\nVerificando banco...\n")

conexao = sqlite3.connect("database/monitor.db")

cursor = conexao.cursor()

cursor.execute("""
SELECT name 
FROM sqlite_master 
WHERE type='table'
""")

tabelas = cursor.fetchall()

print("Tabelas encontradas:")

for tabela in tabelas:
    print(tabela[0])

conexao.close()