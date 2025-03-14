import os
import sqlite3
import json  # <--- IMPORTANTE para evitar caracteres Unicode escapados
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, jsonify

app = Flask(__name__)
load_dotenv()

# Configuração da API OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Função para buscar dados do cliente no banco de dados
def get_client_data(numero_whatsapp):
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT configuracao FROM clientes WHERE numero_whatsapp = ?", (numero_whatsapp,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return eval(result[0])  # Converte JSON string para dicionário
    return None

# Função para gerar resposta personalizada
def generate_response(user_message, numero_whatsapp):
    cliente_data = get_client_data(numero_whatsapp)
    
    if not cliente_data:
        return "Desculpe, não encontrei informações sobre este cliente."

    context = "\n".join([f"{key}: {value}" for key, value in cliente_data.items()])
    prompt = f"Informações do negócio:\n{context}\n\nUsuário: {user_message}\nChatbot:"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente que responde com base nas informações do cliente."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# Nova rota para testar o chatbot
@app.route("/test", methods=["POST"])
def test_chatbot():
    data = request.get_json()
    user_message = data.get("message", "")
    numero_whatsapp = data.get("numero_whatsapp", "")  # Número do WhatsApp do cliente
    
    response_text = generate_response(user_message, numero_whatsapp)
    
    # 🔹 Convertendo JSON manualmente para evitar caracteres especiais escapados
    response_json = json.dumps({"response": response_text}, ensure_ascii=False)
    
    return response_json, 200, {"Content-Type": "application/json; charset=utf-8"}

from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "token_test_ngrok"  # O mesmo que você colocou no Meta

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token and challenge:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200  # Retorna o challenge corretamente
        else:
            return "Invalid Token", 403  # Mensagem de erro mais clara

    return "Bad Request", 400  # Se faltar algum parâmetro, retorna erro 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
