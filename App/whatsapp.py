from twilio.twiml.messaging_response import MessagingResponse
from collections import defaultdict


helpMessage = """Welcome to Quick Pickup!
*list* - Lists items in cart
*place order* - Place your order
*remove <item number>* - Remove item from your cart
*<item> - <quantity>* - Add item to cart"""

ShoppingList = defaultdict(dict)


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
    if "help" in msg.lower():
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

        # HANDLE ORDERING HERE
        # SEND TO FRONT END
        ShoppingList[sender] = {}
        return (
            "Your order has been placed successfully!\n"
            + "Items in current order:\n"
            + getAllItems()
        )

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
