from App.whatsapp import addOrder


def mockOrders():
    addOrder({"Eggs": 5, "Bread": 1, "Detergent": 2}, "NUMBER_REMOVED")
    addOrder({"Garlic": 10, "Apples": 5, "Oreos": 2, "Donuts": 24}, "NUMBER_REMOVED")
    addOrder(
        {
            "Apples": 5,
            "Oranges": 4,
            "Pineapples": 1,
            "Oreo packs": 2,
            "Donuts": 24,
            "Cereal": 2,
            "Licorice": 5,
            "Detergent": 1,
        },
        "NUMBER_REMOVED",
    )
