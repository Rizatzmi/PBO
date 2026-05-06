class hero():
    def __init__(self, namahero, health, power, armor):
        self.name = namahero
        self.health = health
        self.power = power
        self.armor = armor

hero1 = hero("Dwi Putra", 100, 50, 20)
hero2 = hero("Andini", 80, 60, 30)
hero3 = hero("Dwi Putri", 90, 55, 25)
hero4 = hero("Rizqi", 110, 45, 15)
hero5 = hero("Dwi", 95, 65, 35)

print(hero1.__dict__)
print(hero2.__dict__)
print(hero3.__dict__)
print(hero4.__dict__)
print(hero5.__dict__)

