import random
import math
import json
import time

monsters = {
    "Goblin": {"lvh": 20, "lvl": 1,"hp": 20, "atk": 10, "df": 10, "spd": 20, "xpdf": 5, "g": 5},
    "Bush Ambusher": {"lvh": 25, "lvl": 2,"hp": 20, "atk": 25, "df": 5, "spd": 40, "xpdf": 10, "g": 5},
    "Spirit": {"lvh": 25, "lvl": 3,"hp": 40, "atk": 5, "df": 20, "spd": 40, "xpdf": 10, "g": 10},
    "Wolf": {"lvh": 30, "lvl": 5,"hp": 60, "atk": 30, "df": 10, "spd": 30, "xpdf": 15, "g": 15},
    "Bandit": {"lvh": 35, "lvl": 10,"hp": 30, "atk": 25, "df": 10, "spd": 40, "xpdf": 20, "g": 25},
    "Forest Spirit": {"lvh": 40, "lvl": 10,"hp": 45, "atk": 10, "df": 30, "spd": 45, "xpdf": 15, "g": 15},
}

lvtemp = None
goldtemp = None
player_temp_hp = None
monster_temp_hp = None
win = None


class Player:
    def __init__(self, name, class_type, lv, xp, hp, atk, df, spd, gold, upg_pts, ready):
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
        self.ready = ready

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
    
    def gain(self, monlv, xp, gold):
        global lvtemp, goldtemp
        lvtemp = self.lv
        goldtemp = self.gold
        if monlv == 0:
            self.xp += xp
            self.gold += gold
        else:
            self.xp += round(xp*(1/(self.lv/(self.lv/abs(self.lv-(monlv+1))))))
            self.gold += round(gold*(1/(self.lv/(self.lv/abs(self.lv-(monlv+1))))))
            print(self.xp)
            print(self.gold)
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
        self.xp = xp + lv
        self.hp = hp + lv
        self.atk = atk + lv
        self.df = df + lv
        self.spd = spd + lv
        self.gold = g + lv

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

def choose_class(name, num):
    global User
    if num == "1":
        User = Player(name, "Berserker", 1, 0, 20, 20, 5, 10, 0, 6, False)
        return "Berserker"
    elif num == 2:
        User = Player(name, "Mage", 1, 0, 20, 10, 10, 10, 0, 6, False)
        return "Mage"
    elif num == 3:
        User = Player(name, "Healer", 1, 0, 30, 15, 10, 10, 0, 6, False)
        return "Healer"
    else:
        return False

def battle(playerhp, playeratk, playerdf, monsterhp, monsteratk, monsterdf, monstername):
    global player_temp_hp, monster_temp_hp, win
    player_temp_hp = playerhp
    monster_temp_hp = monsterhp
    while True:
        damage_to_monster = max(1, playeratk - random.randint(1, monsterdf))
        monster_temp_hp -= damage_to_monster
        print(f"You dealt {damage_to_monster} damage to {monstername}. Monster HP is now {max(0, monster_temp_hp)}.")
        if monster_temp_hp <= 0:
            print("You defeated the monster!")
            win = True
            return True
        damage_to_player = max(1, monsteratk - random.randint(1, playerdf))
        player_temp_hp -= damage_to_player
        print(f"{monstername} dealt {damage_to_player} damage to you. Your HP is now {max(0, player_temp_hp)}.")
        if player_temp_hp <= 0:
            print("You were defeated by the monster.")
            win = False
            return False
        time.sleep(1)

def apply_points():
    while User.upg_pts > 0:
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
            if int(how_much) <= User.upg_pts:
                User.apply_pts(int(how_much), type_chosen)
                break
            else:
                print("You don't have this much.")

def show_stats():
    print(f"Level: {User.lv}")
    print(f"XP: {User.xp}/{User.lv+1}")
    print(f"HP: {User.hp}")
    print(f"ATK: {User.atk}")
    print(f"DEF: {User.df}")
    print(f"SPD: {User.spd}")
    print(f"Gold: {User.gold}")
    print(f"Upgrade Points: {User.upg_pts}")

def new_player():
    print("Save does not exist.")
    print("New user detected. Welcome to Battle World!")
    print("Battle World is a text-based RPG where you can fight monsters, level up, and become stronger!")
    name = input("Please enter your name: ")
    while True:
        print("Welcome to Battle World! Please choose your class(enter the corresponding number).")
        class_num = input("1. Berserker High Speed and Damage. 2. Mage High Speed and Defense 3. Healer Heals or Poisons and high defense ")
        class_type = choose_class(name, class_num)
        if class_type:
            print(f"You chose {class_type}!")
            break
        else:
            print("Not a valid selection")
    print("You have 6 upgrade points. You can apply them on things like HP, ATK, DEF, SPD, or your gold. Each point increases each stat by 1, but gold increases by 2. Choose wisely.")
    print("Which attribute do you want to put points on? Remember, you can put points on many different things.")
    apply_points()
    print("Done! You have finished setting up. Welcome to Battle World! Please restart the game to load your save.")    
    save()

def save():
    data = {
        "name": User.name,
        "class_type": User.class_type,
        "lv": User.lv,
        "xp": User.xp,
        "hp": User.hp,
        "atk": User.atk,
        "df": User.df,
        "spd": User.spd,
        "gold": User.gold,
        "upg_pts": User.upg_pts,
        "ready": User.ready
    }
    with open("data.json", "w") as f:
        json.dump(data, f)

def load_save():
    global User
    data = json.load(f)
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
    ready = data["ready"]
    User = Player(name, class_type, lv, xp, hp, atk, df, spd, gold, upg_pts, ready)

def start_tutorial():
    print("Welcome to Battle World!")
    time.sleep(1)
    print("Lets start with the basics.")
    time.sleep(1)
    print("You can fight monsters to gain experience and gold. Level up to become stronger!")
    time.sleep(1)
    print(f"Your current stats are:")
    time.sleep(1)
    show_stats()
    time.sleep(5)
    print("These are all the stats. If you're wondering, speed indicates how fast you can flee from a monster.")
    print("Now, lets get a monster to fight.")
    time.sleep(1)
    intro_monster = Monster(list(monsters.keys())[0], monsters["Goblin"]["lvl"], monsters["Goblin"]["xpdf"], monsters["Goblin"]["hp"], monsters["Goblin"]["atk"], monsters["Goblin"]["df"], monsters["Goblin"]["spd"], monsters["Goblin"]["g"])
    while True:
        print(f"A wild {intro_monster.name} has appeared!")
        time.sleep(0.5)
        print("Prepare for battle!")
        time.sleep(0.5)
        battle(User.hp, User.atk, User.df, intro_monster.hp, intro_monster.atk, intro_monster.df, intro_monster.name)
        if win:
            gain(intro_monster)
            print("You have completed the tutorial!")
            break
        else:
            print("You have failed the tutorial. Please restart the game to try again.")
            break

def gain(monster):
    monlv, xp_gain, gold_gain = monster.die()
    User.gain(monlv, xp_gain, gold_gain)

while True:
    try:
        with open("data.json", "r") as f:
            load_save()
            if User.ready == False:
                start_tutorial()
                User.ready = True
                break
            else:
                print("Save loaded successfully!")
                break
                
    except FileNotFoundError:
        new_player()
        break

while User.ready == True:
    save()
    action = input("What do you want to do? 1. Adventure 2. Apply points 3. Shop 4. View stats: ")
    if action == "1":
        pass
    elif action == "2":
        if User.upg_pts == 0:
            print("You don't have any upgrade points.")
        else:
            apply_points()
    elif action == "3":
        apply_points()
    elif action == "4":
        print("Your stats(enter e to exit):")
        time.sleep(1)
        show_stats()
        while True:
            choice = input(" ")
            if choice == "e":
                break
            else:
                pass