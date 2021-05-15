from flask import Flask
from flask.globals import request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)

ShoppingLists = {}


@app.route("/")
def index():
    return "Hello, Potato!"


@app.route("/message", methods=["POST"])
def reply_message():
    msg = request.form.get("Body")
    sender = request.form.get("From").split(":")[1].replace("+", "")
    print(sender)
    response = MessagingResponse()
    global ShoppingLists
    if "help" in msg.lower():
        response.message(
            """Welcome to Quick Pickup!
            *list* - Lists items in cart
            *place order* - Place your order
            *remove <item number>* - Remove item from your cart
            *<item> - <quantity>* - Add item to cart"""
        )
    if msg.lower() == "list":
        if sender not in ShoppingLists:
            response.message("Your cart is empty!")
        else:
            response.message("\n".join(ShoppingLists[sender]))

    if "-" in msg:
        if sender not in ShoppingLists:
            ShoppingLists[sender] = msg.splitlines()
            response.message("Added item to cart!")
        else:
            ShoppingLists[sender] += msg.splitlines()
            response.message("Added item to cart!")

    if msg.lower() == "place order":
        response.message(
            """Your order has been placed successfully!
            Items in current order:
            {}""".format(
                "\n".join(ShoppingLists[sender])
            )
        )
        ShoppingLists.pop(sender)

    if (
        msg.lower().startswith("remove")
        and int(msg.split(" ")[1].strip(" ")) >= 1
        and int(msg.split(" ")[1].strip(" ")) <= len(ShoppingLists[sender])
    ):
        ShoppingLists[sender].pop(int(msg.split(" ")[1].strip(" ")) - 1)

    return str(response)


if __name__ in "__main__":
    app.run()
