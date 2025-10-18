import random
import math
import json

monsters = {
    "Goblin": {"lvh": 20, "lvl": 1,"hp": 50, "atk": 20, "df": 15, "spd": 35, "xpdf": 5, "g": 5},
    "Bush Ambusher": {"lvh": 25, "lvl": 2,"hp": 30, "atk": 25, "df": 5, "spd": 40, "xpdf": 10, "g": 5},
    "Spirit": {"lvh": 25, "lvl": 3,"hp": 40, "atk": 5, "df": 20, "spd": 40, "xpdf": 10, "g": 10},
    "Wolf": {"lvh": 30, "lvl": 4,"hp": 60, "atk": 30, "df": 10, "spd": 30, "xpdf": 15, "g": 15},
    "Bandit": {"lvh": 35, "lvl": 5,"hp": 30, "atk": 25, "df": 10, "spd": 40, "xpdf": 20, "g": 25},
}

lvtemp = None
goldtemp = None
player_temp_hp = None
monster_temp_hp = None

class Player:
    def __init__(self, name, class_type, lv, xp, hp, atk, df, spd, gold, upg_pts):
        self.name = name
        self.class_type = class_type
        self.lv = lv
        self.xp = xp
        self.hp = hp
        self.atk = atk
        self.df = df
        self.spd = spd
        self.gold = gold
        self.upg_pts = upg_pts

    def level_up(self):
        self.lv += 1
        if self.class_type == "Berserker":
            self.hp += 3+math.floor(self.lv/5)
            self.atk += 4+math.floor(self.lv/10)
            self.df += 1+math.floor(self.lv/20)
            self.spd += 2+math.floor(self.lv/20)
            self.upg_pts += 1+math.floor(self.lv/10)
        elif self.class_type == "Mage":
            self.hp += 3+math.floor(self.lv/5)
            self.atk += 2+math.floor(self.lv/10)
            self.df += 2+math.floor(self.lv/20)
            self.spd += 4+math.floor(self.lv/20)
            self.upg_pts += 1+math.floor(self.lv/10)
        elif self.class_type == "Healer":
            self.hp += 4+math.floor(self.lv/5)
            self.atk += 3+math.floor(self.lv/10)
            self.df += 3+math.floor(self.lv/20)
            self.spd += 2+math.floor(self.lv/20)
            self.upg_pts += 1+math.floor(self.lv/10)
        print(f"{self.name} leveled up to {self.lv}!")
    
    def apply_pts(self, amount, attribute):
        self.upg_pts -= amount
        if self.upg_pts >= 0:
            if attribute != "gold":
                self.__dict__[attribute] += amount
                print(f"You increased {attribute} by {amount}! It is now {self.__dict__[attribute]}")
            else:
                self.gold += amount*2
                print(f"You increased your gold by {attribute*2}!")
        else:
            print("Not enough upgrade points.")
    
    def gain(self, lv, xp, gold):
        global lvtemp, goldtemp
        lvtemp = self.lv
        goldtemp = self.gold
        if lv == 0:
            self.xp += xp
            self.gold += gold
        else:
            self.xp += math.round(xp*(1/(self.lv/(self.lv/(self.lv-lv)))))
            self.gold += math.round(gold*(1/(self.lv/(self.lv/(self.lv-lv)))))
        while self.xp >= self.lv+1:
            self.xp -= (self.lv+1)
            self.level_up()
        if self.lv > lvtemp:
            print(f"Congrats! You have leveled up to {self.lv}")
            lvtemp = 0
        if self.gold > goldtemp:
            print(f"You have gained {self.gold - goldtemp} gold.")
            goldtemp = 0

class Monster:
    def __init__(self, monster, lv, xp, hp, atk, df, spd, g):
        self.name = monster
        self.lv = lv
        self.xp = xp
        self.hp = hp
        self.atk = atk
        self.df = df
        self.spd = spd
        self.gold = g

    def die(self):
        return self.lv, self.xp, self.gold
    
    def battle(self):
        return self.lv, self. hp, self.atk, self.df, self.spd
    
def choose_attribute_add(num):
    if num == "1":
        return "hp"
    elif num == "2":
        return "atk"
    elif num == "3":
        return "df"
    elif num == "4":
        return "spd"
    elif num == "5":
        return "gold"
    else:
        return False

def choose_class(num):
    global Player
    if num == "1":
        Player = Player(name, "Berserker", 1, 0, 20, 20, 5, 10, 0, 6)
        return "Berserker"
    elif num == 2:
        Player = Player(name, "Mage", 1, 0, 25, 10, 10, 10, 0, 6)
        return "Mage"
    elif num == 3:
        Player = Player(name, "Healer", 1, 0, 20, 10, 10, 10, 0, 6)
        return "Healer"
    else:
        return False
while True:
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            print("Save loaded successfully!")
            name = data["name"]
            class_type = data["class_type"]
            lv = data["lv"]
            xp = data["xp"]
            hp = data["hp"]
            atk = data["atk"]
            df = data["df"]
            spd = data["spd"]
            gold = data["gold"]
            upg_pts = data["upg_pts"]
            Player = Player(name, class_type, lv, xp, hp, atk, df, spd, gold, upg_pts)
    except FileNotFoundError:
        name = input("Save does not exist. New user detected. Please enter your name: ")
        while True:
            print("Welcome to Battle World! Please choose your class(enter the corresponding number).")
            class_num = input("1. Berserker High Speed and Damage. 2. Mage High Speed and Defense 3. Healer Heals or Poisons and high defense ")
            class_type = choose_class(class_num)
            if class_type:
                print(f"Congrats! You chose {class_type}!")
                break
            else:
                print("Not a valid selection")
        print("You have 6 upgrade points. You can apply them on things like HP, ATK, DEF, SPD, or your gold. Each point increases each stat by 1, but gold increases by 2. Choose wisely.")
        print("Which attribute do you want to put points on? Remember, you can put points on many different things.")
        while Player.upg_pts > 0:
            type_chosen = None
            choose_attr = input("Enter the corresponding number: 1. HP 2. ATK 3. DEF 4. SPD 5. Gold ")
            while True:
                type_chosen = choose_attribute_add(choose_attr)
                if type_chosen:
                    break
                else:
                    print("Invalid choice.")
            print(f"You have chosen {type_chosen}!")
            while True:
                how_much = input(f"Choose the amount of points you want to apply(If you change your mind, enter 0): ")
                if int(how_much) <= Player.upg_pts:
                    Player.apply_pts(int(how_much), type_chosen)
                    break
                else:
                    print("You don't have this much.")
        print("Done! You have finished setting up. Welcome to Battle World! Please restart the game to load your save.")    
        data = {
            "name": Player.name,
            "class_type": Player.class_type,
            "lv": Player.lv,
            "xp": Player.xp,
            "hp": Player.hp,
            "atk": Player.atk,
            "df": Player.df,
            "spd": Player.spd,
            "gold": Player.gold,
            "upg_pts": Player.upg_pts
        }
    with open("data.json", "w") as f:
        json.dump(data, f)
        break