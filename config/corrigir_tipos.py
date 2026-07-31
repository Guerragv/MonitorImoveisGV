import sqlite3

conn = sqlite3.connect("database/monitor.db")

cursor = conn.cursor()


cursor.execute("""
UPDATE imoveis
SET tipo_imovel = 'Apartamento'
WHERE titulo LIKE '%Apartamento%'
""")

cursor.execute("""
UPDATE imoveis
SET tipo_imovel = 'Casa'
WHERE titulo LIKE '%Casa%'
""")

cursor.execute("""
UPDATE imoveis
SET tipo_imovel = 'Loja'
WHERE titulo LIKE '%Loja%'
""")

cursor.execute("""
UPDATE imoveis
SET tipo_imovel = 'Kitnet'
WHERE titulo LIKE '%Kitnet%'
""")

cursor.execute("""
UPDATE imoveis
SET tipo_imovel = 'Sala'
WHERE titulo LIKE '%Sala%'
""")


conn.commit()

conn.close()

print("Tipos corrigidos com sucesso!")