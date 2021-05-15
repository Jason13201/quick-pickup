from flask import request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from twilio.twiml.messaging_response import MessagingResponse

from App import app
from App.whatsapp import handleWAMessage
from App.models import User


@app.route("/")
def index():
    if current_user.is_authenticated:
        return "Hello, not a potato!"
    return "Hello, Potato!"


@app.route("/login")
def login():
    login_user(User(0))
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/message", methods=["POST"])
def reply_message():
    response = MessagingResponse()

    response.message(handleWAMessage(request.form.get("Body"), request.form.get("From")))
    return str(response)
