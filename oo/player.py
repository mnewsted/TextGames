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

    def add_health(self, amount):
        self.hp += amount
        if self.hp > 100:
            self.hp = 100

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            print('That was a fatal blow.')

    def is_dead(self):
        return self.hp <= 0

    def show_inventory(self):
        if self.has_things():
            print('You are carrying:')
            for thing in self.inventory:
                if thing['on_person']:
                    print(thing['prefix'].capitalize() + ' ' + thing['name'])
        else:
            print('You aren\'t carrying anything.')

    def delete_thing(self, thing_name):
        for thing in self.inventory:
            if thing['name'] == thing_name and thing['on_person']:
                self.inventory.remove(thing)

    def add_thing(self, thing):
        self.inventory.append(thing)

    def inventory_size(self):
        return len(self.inventory)

    def has_things(self):
        return self.inventory_size() > 0

    def has_thing(self, thing):
        return thing in self.inventory
