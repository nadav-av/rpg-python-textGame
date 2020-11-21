import random


class Spell:
    def __init__(self, name, cost, dmg, var):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.var = var

    def get_name(self):
        return self.name

    def get_cost(self):
        return self.cost

    def generate_damage(self):
        low = self.dmg - 15
        high = self.dmg + 15
        return random.randrange(low, high)

