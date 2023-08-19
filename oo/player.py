class Player:

    maxHealth = 100

    def __init__(self):
        self.hp = self.maxHealth
        self.inventory = []

    def to_max_health(self):
        self.hp = self.maxHealth

    def wellness(self):
        percentage = self.hp / self.maxHealth * 100
        if percentage > 75:
            print("You are in good shape.")
        elif percentage > 50:
            print("You are in pain.")
        elif percentage > 25:
            print("You are hurting but still able to fight.")
        elif percentage > 0:
            print("You are seriously wounded.")
        else:
            print("You are dead.")

    def addHealth(self, amount):
        self.hp += amount
        if self.hp > 100:
            self.hp = 100

    def takeDamage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            print('That was a fatal blow.')

    def is_dead(self):
        return self.hp <= 0