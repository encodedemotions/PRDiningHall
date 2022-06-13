import json

class RestaurantMenu:
    def __init__(self) -> None:
        self.foods = []

        with open('menu.json') as file:
            data  = json.load(file)

        self.foods = data
