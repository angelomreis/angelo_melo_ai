from flask import Blueprint, request

webhook_bp = Blueprint("webhook", __name__)

VERIFY_TOKEN = "token_meta_business"

@webhook_bp.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token and challenge:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200  # Retorna o challenge corretamente
        else:
            return "Invalid Token", 403

    return "Bad Request", 400
