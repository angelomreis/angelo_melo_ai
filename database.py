import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Conectar ao banco de dados PostgreSQL
def connect_db():
    return psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")

# Criar a tabela se não existir
def setup_database():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            numero_whatsapp TEXT UNIQUE NOT NULL,
            configuracao TEXT NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Função para buscar dados do cliente no banco
def get_client_data(numero_whatsapp):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT configuracao FROM clientes WHERE numero_whatsapp = %s", (numero_whatsapp,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return json.loads(result[0])  # Converte JSON string para dicionário
    return None

# Função para adicionar um cliente ao banco de dados
def add_client(numero_whatsapp, configuracao):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO clientes (numero_whatsapp, configuracao) VALUES (%s, %s) ON CONFLICT (numero_whatsapp) DO UPDATE SET configuracao = EXCLUDED.configuracao;",
        (numero_whatsapp, json.dumps(configuracao))
    )
    
    conn.commit()
    cursor.close()
    conn.close()

# Só executa a criação da tabela se rodado diretamente
if __name__ == "__main__":
    setup_database()
    
    # Adicionando um cliente de teste
    client_data = {
        "horario": "Nosso horário de funcionamento é das 8h às 18h.",
        "endereco": "Estamos localizados na Rua Exemplo, 123 - Centro.",
        "servicos": "Oferecemos hospedagem, café da manhã e passeios turísticos."
    }
    
    add_client("+55 99999-9999", client_data)
    print("Cliente adicionado com sucesso!")
