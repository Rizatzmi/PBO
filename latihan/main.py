class Hero:

    __jumlah = 0

    def __init__(self, name, health, attack, armor):
        self.__name = name
        self.__healthBase = health
        self.__attack = attack
        self.__armor = armor
        self.__level = 1
        self.__exp = 0

        self.__healthMax = self.__healthBase * self.__level
        self.__attPower = self.__attack * self.__level
        self.__armorPower = self.__armor * self.__level

        self.__health = self.__healthMax
        Hero.__jumlah += 1

    @property
    def info(self):
        return "{} level {}: \n\thealth = {}/{} \n\tattack = {} \n\tarmor = {}".format(self.__name, self.__level, self.__health, self.__healthMax, self.__attPower, self.__armorPower)

    @property
    def gainExp(self):
        pass

    @gainExp.setter
    def gainExp(self, addExp):
        self.__exp += addExp
        if self.__exp >= 100:
            print(self.__name, "level up!")
            self.__level += 1
            self.__exp -= 100
            self.__healthMax = self.__healthBase * self.__level
            self.__attPower = self.__attack * self.__level
            self.__armorPower = self.__armor * self.__level
    
    def attack(self, target):
        self.gainExp = 50

slardar = Hero("Slardar", 100, 5, 10)
axe = Hero("Axe", 100, 7, 5)
print(slardar.info)

slardar.attack(axe)
slardar.attack(axe)
slardar.attack(axe)
slardar.attack(axe)
slardar.attack(axe)
slardar.attack(axe)
print(slardar.info)