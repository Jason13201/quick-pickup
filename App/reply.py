from config import auth_token, account_sid
from twilio.rest import Client

client = Client(account_sid, auth_token)


def sendWAMessage(to, message):
    client.messages.create(
        from_="whatsapp:+14155238886",
        body=message,
        to=to,
    )
