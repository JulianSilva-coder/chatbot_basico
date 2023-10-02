from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from transformers import pipeline
import pandas as pd

# Credenciales de Twilio
account_sid = "AC380b7e610f5afe32e820bb4e80bd2509"
auth_token = "7e10312db955324c0d88b28fe03a1052"

# Número de Twilio de WhatsApp
twilio_number = "whatsapp:+14155238886"
user_number = "whatsapp:+573154235237"

tqa = pipeline(task="table-question-answering", model="google/tapas-base-finetuned-wtq")

table = pd.read_csv("data.csv")
table = table.astype(str)

app = Flask(__name__)

@app.route('/responder', methods=['POST'])
def responder():
    incoming_message = request.values.get('Body', '').lower()

    answer = tqa(table=table, query=incoming_message)["answer"]
    response_message = f"Respuesta a '{incoming_message}': {answer}"

    # Crear una respuesta de TwiML para enviar el mensaje de respuesta
    response = MessagingResponse()
    response.message(response_message)

    return str(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
