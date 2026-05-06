class Hero:
    def __init__(self, name, health, power, armor):
        self.name = name
        self.health = health
        self.power = power
        self.armor = armor

    def siapa(self):
        print("Nama hero : ", self.name)

    def healthup(self, health):
        self.health += health

    def getHealth(self):
        return self.health

superman = Hero("Superman", 100, 50, 20)
batman = Hero("Batman", 80, 40, 30)

superman.siapa()
superman.healthup(20)
print("Health Superman : ", superman.getHealth())
