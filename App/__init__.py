from flask import Flask
from flask.globals import request
from twilio.twiml.messaging_response import MessagingResponse

from App.whatsapp import handleWAMessage


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, Potato!"


@app.route("/message", methods=["POST"])
def reply_message():
    response = MessagingResponse()

    response.message(handleWAMessage(request.form.get("Body"), request.form.get("From")))
    return str(response)
