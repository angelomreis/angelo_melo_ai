from flask import Flask, request, jsonify
from chatbot import generate_response
from webhook import webhook_bp
from database import setup_database
import json

app = Flask(__name__)

# Configurações iniciais
setup_database()
app.register_blueprint(webhook_bp)

# Nova rota para testar o chatbot
@app.route("/test", methods=["POST"])
def test_chatbot():
    data = request.get_json()
    user_message = data.get("message", "")
    numero_whatsapp = data.get("numero_whatsapp", "")

    response_text = generate_response(user_message, numero_whatsapp)

    return json.dumps({"response": response_text}, ensure_ascii=False), 200, {"Content-Type": "application/json; charset=utf-8"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
