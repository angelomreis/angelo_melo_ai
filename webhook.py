import os
import json
import requests
from flask import Blueprint, request, jsonify
from chatbot import generate_response

webhook_bp = Blueprint("webhook", __name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

# 📌 Rota para verificação do webhook
@webhook_bp.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

# 📌 Rota para processar mensagens recebidas
@webhook_bp.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    print("Recebi uma mensagem no webhook:", json.dumps(data, indent=2, ensure_ascii=False))  # <-- Debug para ver a mensagem recebida

    if "entry" in data:
        for entry in data["entry"]:
            if "changes" in entry:
                for change in entry["changes"]:
                    if "value" in change and "messages" in change["value"]:
                        messages = change["value"]["messages"]
                        for message in messages:
                            numero_whatsapp = message["from"]
                            user_message = message["text"]["body"]

                            # 🎯 Chama o ChatGPT para gerar uma resposta
                            response_text = generate_response(user_message, numero_whatsapp)

                            # 📤 Envia a resposta pelo WhatsApp
                            send_whatsapp_message(numero_whatsapp, response_text)

    return jsonify({"status": "success"}), 200

# 📌 Função para enviar mensagem para o WhatsApp
def send_whatsapp_message(to, message):
    url = "https://graph.facebook.com/v19.0/{}/messages".format(os.getenv("WHATSAPP_PHONE_ID"))
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
