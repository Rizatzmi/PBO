class Hero:
    jumlah_hero = 0

    def __init__(self, name, health, power, armor):
        self.name = name
        self.health = health
        self.power = power
        self.armor = armor
        Hero.jumlah_hero += 1

superman = Hero("Superman", 100, 50, 20)
print("===Var Jumlah===")
print("Punya Object : ", superman.jumlah_hero)
print("Punya Class : ", Hero.jumlah_hero)
print("===Nilai Jumlah Hero Object===")
superman.jumlah_hero = 10
print("Punya Object : ", superman.jumlah_hero)
print("Punya Class : ", Hero.jumlah_hero)
print("===Nilai Jumlah Hero Class===")
Hero.jumlah_hero = 20
print("Punya Object : ", superman.jumlah_hero)
print("Punya Class : ", Hero.jumlah_hero)
