from flask import Flask
from flask.globals import request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

@app.route("/message", methods = ['POST'])
def reply_message():
    msg = request.form.get('Body')


    response = MessagingResponse()
    response.message(f"Success! \n {msg}")

    return str(response)


if __name__ in "__main__":
    app.run()