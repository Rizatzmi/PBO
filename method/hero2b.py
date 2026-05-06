class Hero:
    jumlah_hero = 0

    def __init__(self, name, health, power, armor):
        self.name = name
        self.health = health
        self.power = power
        self.armor = armor
        Hero.jumlah_hero += 1
        self.__age = 70
        self._weight = 110

superman = Hero("Superman", 100, 50, 20)
print(superman.__dict__)
print("Umur Superman : ", superman._Hero__age)

superman._Hero__age = 80
print("Umur Superman : ", superman._Hero__age)
print(superman.__dict__)

superman._weight = 120
print("Berat Superman : ", superman._weight)
print(superman.__dict__)

# print(superman.__age)
print(superman._weight)
