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

    if "-" in msg:
        if sender not in ShoppingLists:
            ShoppingLists[sender] = msg.splitlines()
            response.message("Added item to cart!")
        else:
            ShoppingLists[sender] += msg.splitlines()
            response.message("Added item to cart!")

    if (
        msg.lower().startswith("remove")
        and int(msg.split(" ")[1].strip(" ")) >= 1
        and int(msg.split(" ")[1].strip(" ")) <= len(ShoppingLists[sender])
    ):
        ShoppingLists[sender].pop(int(msg.split(" ")[1].strip(" ")) - 1)

    return str(response)
