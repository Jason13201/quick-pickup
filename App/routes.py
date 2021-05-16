from flask import request, redirect, url_for, render_template
from flask_login import login_user, logout_user, current_user, login_required
from flask_socketio import emit
from twilio.twiml.messaging_response import MessagingResponse

from App import app, socketio
from App.whatsapp import handleWAMessage, getOrders, markOrderAsReady, markOrderAsPickedUp
from App.models import User


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("dash.html")
    return render_template("login.html")


@app.route("/login", methods=["POST"])
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


@login_required
@app.route("/orders")
def orders():
    return str(getOrders())


@socketio.on("connect")
def socket_connect():
    emit("orders", getOrders())


@socketio.on("ready")
def socket_order_ready(orderNum):
    markOrderAsReady(orderNum)


@socketio.on("pickedup")
def socket_order_ready(orderNum):
    markOrderAsPickedUp(orderNum)
