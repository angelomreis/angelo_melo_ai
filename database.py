import sqlite3

# Criando o banco de dados
conn = sqlite3.connect("clientes.db")
cursor = conn.cursor()

# Criando a tabela de clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    numero_whatsapp TEXT UNIQUE NOT NULL,
    configuracao TEXT NOT NULL
)
""")

# Adicionando dados de exemplo
cursor.execute("""
INSERT INTO clientes (nome, numero_whatsapp, configuracao) VALUES 
('Pousada Sol Nascente', '+55 99999-9999', '{"horario": "8h às 18h", "endereco": "Rua Exemplo, 123"}'),
('Salão de Beleza Estilo', '+55 88888-8888', '{"horario": "10h às 20h", "servicos": "Corte, escova"}')
""")

conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")
