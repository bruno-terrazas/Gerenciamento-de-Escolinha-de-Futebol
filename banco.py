import sqlite3

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

# ---------- Tabelas ----------

cursor.execute("""CREATE TABLE IF NOT EXISTS categorias(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS modalidades(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                valor_mensal FLOAT NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS atletas(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                data_nascimento TEXT NOT NULL,
                cpf_atleta TEXT NOT NULL UNIQUE,
                pai TEXT NOT NULL,
                mae TEXT NOT NULL,
                cpf_responsavel TEXT NOT NULL,
                endereco TEXT NOT NULL,
                whats TEXT NOT NULL,
                escola TEXT NOT NULL,
                categoria_id INTEGER NOT NULL,
                bolsa INTEGER NOT NULL,
                desconto FLOAT,
                equipe INTEGER NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id))""")

cursor.execute("""CREATE TABLE IF NOT EXISTS relacao_atletas(
                atleta_id INTEGER,
                modalidade_id INTEGER,
                PRIMARY KEY (atleta_id, modalidade_id),
                FOREIGN KEY (atleta_id) REFERENCES atletas(id),
                FOREIGN KEY (modalidade_id) REFERENCES modalidades(id))""")

cursor.execute("""CREATE TABLE IF NOT EXISTS pagamentos(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                atleta_id INTEGER,
                mes_referencia TEXT NOT NULL,
                tipo TEXT NOT NULL,
                valor FLOAT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (atleta_id) REFERENCES atletas(id))""")


# ---------- Dados fixos que o sistema precisa para funcionar ----------
# A ORDEM IMPORTA: os formulários usam ids fixos (categorias 1 a 5,
# modalidades 1 e 2), e o AUTOINCREMENT dá os ids na ordem de inserção.
# Cada bloco só insere se a tabela estiver vazia, então rodar o script
# de novo não duplica nada.

categorias = ["Sub-9", "Sub-11", "Sub-13", "Sub-15", "Sub-17"]

cursor.execute("SELECT COUNT(*) FROM categorias")
if cursor.fetchone()[0] == 0:
    for nome in categorias:
        cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))

modalidades = [("Futsal", 200), ("Futebol de campo", 200)]

cursor.execute("SELECT COUNT(*) FROM modalidades")
if cursor.fetchone()[0] == 0:
    for nome, valor_mensal in modalidades:
        cursor.execute("""INSERT INTO modalidades (nome, valor_mensal)
                        VALUES (?, ?)""", (nome, valor_mensal))

conexao.commit()
conexao.close()