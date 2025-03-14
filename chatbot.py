import os
from openai import OpenAI
from database import get_client_data
from dotenv import load_dotenv

load_dotenv()

# Configuração da API OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
