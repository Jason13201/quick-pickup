from random import randrange
from collections import defaultdict

from App import socketio
from App.reply import sendWAMessage

helpMessage = """Welcome to Quick Pickup!
*list* - Lists items in cart
*help* - Shows this help menu
*place order* - Place your order
*remove _<item>_* - Remove from cart
*_<item>_ - _<quantity>_* - Add item to cart"""

ShoppingList = defaultdict(dict)

# Orders
orders = []
orderNumber = 1


def getOrders():
    global orders
    return orders


def addOrder(cart, owner):
    global orders, orderNumber
    orders.append(
        {
            "items": cart,
            "pin": randrange(1000, 10000),
            "number": orderNumber,
            "state": "ordered",
            "owner": owner,
        }
    )
    orderNumber += 1
    socketio.emit("orders", orders, broadcast=True)


def markOrderAsReady(orderNum):
    for order in orders:
        if order["number"] == orderNum:
            sendWAMessage(
                order["owner"],
                f"Your order #{orderNum} has been successfully packed!\nOrder PIN: {order['pin']}",
            )
            order["state"] = "ready"
            return True
    return False


def markOrderAsPickedUp(orderNum):
    for i, order in enumerate(orders):
        if order["number"] == orderNum:
            sendWAMessage(
                order["owner"],
                f"Your order #{orderNum} has been picked up! Thank you for shopping with us :)",
            )
            del orders[i]
            return True
    return False


# Add some additional orders for testing
from App.mock import mockOrders

mockOrders()


def handleWAMessage(msg, sender):
    global ShoppingList

    def isShoppingListEmpty():
        return not len(ShoppingList[sender])

    def getAllItems():
        return "\n".join([f"{item} - {count}" for item, count in ShoppingList[sender].items()])

    def removeItem(item):
        for key in ShoppingList[sender].keys():
            if key.lower() == item.lower():
                ShoppingList[sender].pop(key)
                return True
        return False

    # sender = request.form.get("From").split(":")[1].replace("+", "")
    print(sender)

    # Help - how to use the bot
    if any([word in msg.lower() for word in ["help", "hello", "hi"]]):
        return helpMessage

    # List - show items in the cart
    if msg.lower() in ["list", "show", "cart"]:
        if isShoppingListEmpty():
            return "Your cart is empty!"

        return getAllItems()

    # Place order
    if "order" in msg.lower():
        if isShoppingListEmpty():
            return "Your cart is empty! You can place an order after adding items to the cart!"

        addOrder(ShoppingList[sender], sender)
        response = (
            "Your order has been placed successfully!\n"
            + "Items in current order:\n"
            + getAllItems()
        )
        ShoppingList[sender] = {}
        return response

    # Remove items
    if msg.lower().startswith("remove"):
        words = msg.split(" ")
        if len(words) == 1:
            return "Syntax: remove ITEM_NAME"

        item = words[1]

        if item == "all":
            ShoppingList[sender] = {}
            return "All items were removed from your cart."

        if not removeItem(item):
            return "This item does not exist in your cart."

        return f"{item} successfully removed from your cart."

    # Add items to cart
    for line in msg.splitlines():
        item, quantity = line.split("-", 1) if "-" in line else (line, 1)
        ShoppingList[sender][item.strip(" ")] = int(quantity)

    print(ShoppingList)

    return "Your cart now contains\n" + getAllItems()
