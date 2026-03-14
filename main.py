import random
import math
import json
import time
import os
import pygame

pygame.mixer.init()

monsters = {
    "Goblin": {"lvh": 20, "lvl": 1,"hp": 15, "atk": 10, "df": 10, "spd": 20, "abilities": {"Smash": {"power": 10, "type": "attack", "cd": 1}}, "abidropchance": 100, "xpdf": 5, "g": 5},
    "Bush Ambusher": {"lvh": 25, "lvl": 2,"hp": 20, "atk": 25, "df": 5, "spd": 40, "abilities": {"Ambush": {"power": 5, "type": "scare", "cd": 2}}, "abidropchance": 25, "xpdf": 10, "g": 5},
    "Spirit": {"lvh": 25, "lvl": 3,"hp": 40, "atk": 30, "df": 20, "spd": 40, "abilities": {"Scare": {"power": 10, "type": "scare", "cd": 2}}, "abidropchance": 5, "xpdf": 10, "g": 10},
    "Wolf": {"lvh": 30, "lvl": 5,"hp": 50, "atk": 50, "df": 20, "spd": 45, "abilities": {"Slice": {"power": 15, "type": "attack", "cd": 2}}, "abidropchance": 10, "xpdf": 10, "g": 15},
    "Bandit": {"lvh": 35, "lvl": 10,"hp": 80, "atk": 80, "df": 30, "spd": 75, "abilities": {"Ambush": {"power": 15, "type": "scare", "cd": 3}}, "abidropchance": 3, "xpdf": 15, "g": 25},
    "Forest Spirit": {"lvh": 40, "lvl": 10,"hp": 220, "atk": 150, "df": 120, "spd": 130, "abilities": {"Scare": {"power": 25, "type": "scare", "cd": 4}}, "abidropchance": 5, "xpdf": 20, "g": 15},
    "Mafia Boss": {"lvh": 50, "lvl": 20,"hp": 270, "atk": 220, "df": 160, "spd": 85, "abilities": {"Punch": {"power": 30, "type": "attack", "cd": 5}}, "abidropchance": 15, "xpdf": 30, "g": 50} 
} 

shopitems = {
    "Stone Sword": {"attack": 5, "critchance": 5, "critdmg": 100, "abilities": {}},
    "Iron Sword": {"attack": 15, "critchance": 10, "critdmg": 100, "abilities": {}},
    "Super Sword": {"attack": 25, "critchance": 20, "critdmg": 100, "abilities": {}},
    "Mega Sword": {"attack": 30, "critchance": 30, "critdmg": 150, "abilities": {"Mega Strike": {"power": 50, "subpower": 0, "type": "sword", "subtype": "dmginc"}}},
    "Hypersword": {"attack": 50, "critchance": 50, "critdmg": 200, "abilities": {"Witherborn": {"power": 100, "subpower": 2, "type": "sword", "subtype": "paralyze"}}},
    "Hyperion": {"attack": 100, "critchance": 100, "critdmg": 300, "abilities": {"Termination": {"power": 200, "subpower": 0, "type": "sword", "subtype": "dmginc"}}}
}

songs = ["MEGALOVANIA", "THE WORLD REVOLVING"]

savepath = "data.json"
lvtemp = None
goldtemp = None
player_temp_hp = None
monster_temp_hp = None
win = None
playerturn = None
monsterturn = None


class Player:
    def __init__(self, name, class_type, lv, xp, hp, atk, df, spd, abilities, gold, upg_pts, ready):
        self.name = name
        self.class_type = class_type
        self.lv = lv
        self.xp = xp
        self.hp = hp
        self.atk = atk
        self.df = df
        self.spd = spd
        self.abilities = abilities
        self.gold = gold
        self.upg_pts = upg_pts
        self.ready = ready

    def level_up(self):
        self.lv += 1
        if self.class_type == "Berserker":
            self.hp += 2+math.floor(self.lv/20)
            self.atk += 3+math.floor(self.lv/25)
            self.df += 1+math.floor(self.lv/30)
            self.spd += 2+math.floor(self.lv/30)
            self.upg_pts += 2+math.floor(self.lv/20)
        elif self.class_type == "Mage":
            self.hp += 1+math.floor(self.lv/20)
            self.atk += 2+math.floor(self.lv/30)
            self.df += 2+math.floor(self.lv/30)
            self.spd += 3+math.floor(self.lv/35)
            self.upg_pts += 2+math.floor(self.lv/20)
        elif self.class_type == "Tank":
            self.hp += 3+math.floor(self.lv/15)
            self.atk += 1+math.floor(self.lv/35)
            self.df += 3+math.floor(self.lv/25)
            self.spd += 2+math.floor(self.lv/30)
            self.upg_pts += 2+math.floor(self.lv/20)
        mult = 1 + self.lv / 1750
        self.hp  = round(self.hp  * mult)
        self.atk = round(self.atk * mult)
        self.df  = round(self.df  * mult)
        self.spd = round(self.spd * mult)
        print(f"{self.name} leveled up to {self.lv}!")
        input("Press enter to continue... ")
    
    def apply_pts(self, amount, attribute):
        self.upg_pts -= amount
        if self.upg_pts >= 0:
            if attribute != "gold":
                self.__dict__[attribute] += amount
                print(f"You increased {attribute} by {amount}! It is now {self.__dict__[attribute]}")
                input("Press enter to continue... ")
            else:
                self.gold += amount*2
                print(f"You increased your gold by {attribute*2}!")
                input("Press enter to continue... ")
        else:
            print("Not enough upgrade points.")
            input("Press enter to continue... ")
    
    def gain(self, monlv, xp, gold, abi, abichance):
        if self.lv-(monlv+1.0001) == 0:
            xp_amount = xp
            gold_amount = gold
        elif self.lv-(monlv+1.0001) > 0.0001:
            xp_amount = round(xp*(1/abs(self.lv-(monlv+1.0001))))
            gold_amount = round(gold*(1/abs(self.lv-(monlv+1.0001))))
        elif self.lv-(monlv+1.0001) < 0.0001:
            xp_amount = round(xp*(1/1.15**round(self.lv-(monlv+1.0001))))
            gold_amount = round(gold*(1/1.15**round(self.lv-(monlv+1.0001))))
        self.xp += xp_amount
        self.gold += gold_amount
        while self.xp >= self.lv+1:
            self.xp -= (self.lv+1)
            self.level_up()
        print(f"Congrats! You have leveled up to {self.lv}")
        input("Press enter to continue... ")
        
        print(f"You have gained {gold_amount} gold and {gold_amount} xp.")
        input("Press enter to continue... ")
        chance = abichance
        rand = random.randint(1, 100)
        if rand <= chance and list(abi.keys())[0] not in self.abilities.keys():
            self.abilities.update(abi)
            print(f"You got {list(abi.keys())[0]}!")
            input("Press enter to continue... ")
    def lose(self):
        gtemp = self.gold
        goldlostrand = random.randint(20, 50)
        self.gold = round(self.gold*(1-(goldlostrand/100)))
        input(f"You were defeated and lost {gtemp-self.gold} gold! Next time, maybe flee if you see a mighty opponent. ")

class Monster:
    def __init__(self, monster, lv, xp, hp, atk, df, spd, abilities, abichance, g):
        self.name = monster
        self.lv = lv
        self.xp = xp + round(1.15**lv)
        self.hp = hp + round(1.15**lv)
        self.atk = atk + round(1.15**lv)
        self.df = df + round(1.15**lv)
        self.spd = spd + round(1.15**lv)
        self.abilities = abilities
        self.abichance = abichance
        self.gold = g + round(1.15**lv)

    def die(self):
        return self.lv, self.xp, self.gold, self.abilities, self.abichance
    
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
        User = Player(name, "Berserker", 1, 0, 20, 20, 5, 10, {}, 0, 6, False)
        return "Berserker"
    elif num == "2":
        User = Player(name, "Mage", 1, 0, 20, 15, 10, 10, {}, 0, 6, False)
        return "Mage"
    elif num == "3":
        User = Player(name, "Tank", 1, 0, 35, 10, 15, 5, {}, 0, 6, False)
        return "Tank"
    else:
        return False

def battle(playerhp, playeratk, playerdf, playerabi, playerspd, monsterhp, monsteratk, monsterdf, monsterabi, monstername, monsterlevel, monsterspd):
    global player_temp_hp, monster_temp_hp, win, playerturn, monsterturn, playerstunsuccess, monsterstunsuccess, playertimesstunned, monstertimesstunned
    appearing_dialogues = [f"A wild level {monsterlevel} {monstername} has appeared!", f"Beware... a level {monsterlevel} {monstername} has appeared!", f"You stumble across a level {monsterlevel} {monstername}!"]
    dialogue_rand = random.randint(1, len(appearing_dialogues))
    player_temp_hp = playerhp
    monster_temp_hp = monsterhp
    playerstunsuccess = False
    monsterstunsuccess = False
    playerallincd = False
    monallincd = False
    print(appearing_dialogues[dialogue_rand-1])
    time.sleep(0.5)
    choice = input("Do you Fight or Flee? (1/2) ")
    if User.ready:
        if choice == "1":
            print("Prepare for battle!")
            time.sleep(0.5)
            if playerabi != None:
                playerabicd = {}
                playerabicdtemp = {}
                playerabilist = list(playerabi)
                for i in range(len(playerabi)):
                    playerabicd[playerabilist[i]] = playerabi[playerabilist[i]]["cd"]
                    playerabicdtemp[playerabilist[i]] = 0
            monabicd = {}
            monabicdtemp = {}
            monabilist = list(monsterabi)
            for i in range(len(monsterabi)):
                monabicd[monabilist[i]] = monsterabi[monabilist[i]]["cd"]
                monabicdtemp[monabilist[i]] = 0
            while True:
                playertimesstunned = 0
                monstertimesstunned = 0
                playerturn = False
                monsterturn = False
                playerstunsuccess = False
                monsterstunsuccess = False
                if playerabi == None:
                    pass
                elif not playerallincd:
                    while True:
                        abi = input(f"Which ability do you want to use? {list(playerabicdtemp)} ")
                        if abi in playerabi.keys():
                            if playerabicdtemp[abi] == 0:
                                if playerabi[abi]["type"] == "attack":
                                    playeratk = round(playeratk * (1+(playerabi[abi]["power"]/100)))
                                    break
                                elif playerabi[abi]["type"] == "scare":
                                    playeratk = round(playeratk * (1+(monsterabi[monabinum]["power"]/150)))
                                    stunchance = monsterabi[monabinum]["power"]
                                    damage_to_monster = max(1, playeratk - random.randint(1, monsterdf))
                                    monster_temp_hp -= damage_to_monster
                                    while monster_temp_hp > 0:
                                        pRand = random.randint(1, 100)
                                        if pRand <= stunchance:
                                            damage_to_monster = max(1, playeratk - random.randint(1, monsterdf))
                                            monster_temp_hp -= damage_to_monster
                                            playerstunsuccess = True
                                            playertimesstunned += 1
                                        else:
                                            playerturn = False
                                            monsterturn = True
                                            playerstunsuccess = False
                                            break
                                    break
                            else:
                                input("Please choose another ability, this one is on cooldown.")
                        else:
                            input("Please select a valid option.")
                    for i in range(len(playerabi)):
                        if playerabicdtemp[playerabilist[i]] != 0:
                            playerabicdtemp[playerabilist[i]] -= 1
                        else: 
                            pass
                    playerabicdtemp[abi] = playerabi[abi]["cd"]
                    for i in range(len(playerabi)):
                        if playerabicdtemp[playerabilist[i]] == 0:
                            playerallincd = False
                        else:
                            playerallincd = True
                else:
                    input("All your abilities are on cooldown.")
                if not monsterturn:
                    damage_to_monster = max(1, playeratk - random.randint(1, monsterdf))
                    monster_temp_hp -= damage_to_monster
                if playerabi != None and playerabi[abi]["type"] != "scare": # ability type other than scare
                    input(f"You used {abi} and dealt {damage_to_monster} damage to {monstername}. Monster HP is now {max(0, monster_temp_hp)}.")
                elif playerabi != None and playerstunsuccess: # succesfully scared
                    input(f"You used {abi} and stunned {monstername} {playertimesstunned} time(s). You dealt {damage_to_monster} damage to {monstername} {playertimesstunned + 1} times. Monster HP is now {max(0, monster_temp_hp)}.")
                elif playerabi != None and not playerstunsuccess: # scare ability but failed to scare
                    input(f"You tried using {abi} to scare the monster but you failed. You dealt {damage_to_monster} damage to {monstername}. Monster HP is now {max(0, monster_temp_hp)}.")
                elif playerabi == None: # no ability
                    input(f"You dealt {damage_to_monster} damage to {monstername}. Monster HP is now {max(0, monster_temp_hp)}.")
                else: # this should never happen
                    input("BUG DETECTED (PLAYER)")
                if monster_temp_hp <= 0:
                    input("You defeated the monster!")
                    win = True
                    return True
                if not monallincd:
                    monlist = list(monsterabi.keys())
                    monabinum = monlist[0]
                    if monsterabi[monabinum]["type"] == "attack":
                        monsterdmg = round(monsteratk * (1+(monsterabi[monabinum]["power"]/100)))
                    elif monsterabi[monabinum]["type"] == "scare":
                        monsterdmg = round(monsteratk * (1+(monsterabi[monabinum]["power"]/150)))
                        stunchance = monsterabi[monabinum]["power"]
                        damage_to_player = max(1, monsterdmg - random.randint(1, playerdf))
                        player_temp_hp -= damage_to_player
                        while player_temp_hp > 0:
                            mRand = random.randint(1, 100)
                            if mRand <= stunchance:
                                damage_to_player = max(1, monsteratk - random.randint(1, playerdf))
                                player_temp_hp -= damage_to_player
                                monsterstunsuccess = True
                                monstertimesstunned += 1
                            else:
                                monsterturn = False
                                playerturn = True
                                monsterstunsuccess = False
                                break
                    monabicdtemp[monabinum] = monsterabi[monabinum]["cd"]
                    monallincd = True

                else:
                    damage_to_player = max(1, monsteratk - random.randint(1, playerdf))
                    player_temp_hp -= damage_to_player
                if monabicdtemp[monabilist[0]] != 0:
                    monabicdtemp[monabilist[0]] -= 1
                if monabicdtemp[monabilist[0]] == 0:
                    monallincd = False
                if monsterabi[monabinum]["type"] != "scare": # ablity other than scare
                    input(f"{monstername} used {monabinum} and dealt {damage_to_player} damage to you. Your HP is now {max(0, player_temp_hp)}.")
                elif monsterstunsuccess: # if stunned successfully
                    input(f"{monstername} used {monabinum} and stunned you {monsterstunsuccess} time(s). It dealt {damage_to_player} damage to you {monsterstunsuccess + 1} times. Your HP is now {max(0, player_temp_hp)}.")
                elif not monsterstunsuccess: # used scare ability but failed to stun
                    input(f"{monstername} tried using {monabinum} to scare you but failed. It dealt {damage_to_player} damage to you. Your HP is now {max(0, player_temp_hp)}.")
                elif monallincd:
                    input(f"{monstername} tried using their ability but it was on cooldown ({(monabicdtemp[monabilist[0]])+1} turns left). It dealt {damage_to_player} damage to you. Your HP is now {max(0, player_temp_hp)}.")
                else: # this should never happen
                    print("BUG DETECTED (MONSTER)")
                if player_temp_hp <= 0:
                    input("You were defeated by the monster.")
                    win = False
                    return False
                input("Press enter to continue... ")
        elif choice == "2":
            input("You have chosen to flee!")
            fleechance = round(((monsterspd/playerspd)**-2)/2)
            input(f"Your chance of succeeding is {fleechance}!")
            for i in range(random.randint(1,3)):
                print("Fleeing.")
                time.sleep(1)
                print("Fleeing..")
                time.sleep(1)
                print("Fleeing...")
                time.sleep(1)
            if fleechance < 1:
                randflee = random.randint(1, 100)
                if randflee <= fleechance*100:
                    input("Congrats! You've successfully fleed from the monster! ")
                    return None
                else:
                    input("Oh no! You failed to flee and was caught by the monster. ")
                    win = False
                    return False
            else:
                input("Congrats! You've successfully fleed from the monster! ")
                return None
        
                

def apply_points():
    if User.upg_pts > 0:
        show_stats()
        type_chosen = None
        choose_attr = input("Enter the corresponding number: 1. HP 2. ATK 3. DEF 4. SPD 5. Gold ")
        while True:
            type_chosen = choose_attribute_add(choose_attr)
            if type_chosen:
                break
            else:
                input("Invalid choice.")
        input(f"You have chosen {type_chosen}!")
        while True:
            try:
                how_much = input(f"Choose the amount of points you want to apply(If you change your mind, enter 0): ")
                if int(how_much) <= User.upg_pts:
                    User.apply_pts(int(how_much), type_chosen)
                    break
                else:
                    input("You don't have this much.")
            except ValueError:
                input("Not a valid number.")
    else:
        input("You don't have any points.")

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
    input("New user detected. Welcome to Battle World! (Press enter to continue)")
    input("Battle World is a text-based RPG where you can fight monsters, level up, and become stronger!")
    name = input("Please enter your name: ")
    while True:
        print("Welcome to Battle World! Please choose your class(enter the corresponding number).")
        class_num = input("1. Berserker: High Speed and Damage. 2. Mage: High Speed and Defense 3. Tank: High HP and Defense: ")
        class_type = choose_class(name, class_num)
        if class_type:
            print(f"You chose {class_type}!")
            break
        else:
            print("Not a valid selection")
    print("You have 6 upgrade points. You can apply them on things like HP, ATK, DEF, SPD, or your gold. Each point increases each stat by 1, but gold increases by 2. Choose wisely.")
    print("Which attribute do you want to put points on? Remember, you can put points on many different things.")
    while User.upg_pts > 0:
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
        "abilities": User.abilities,
        "gold": User.gold,
        "upg_pts": User.upg_pts,
        "ready": User.ready
    }
    with open("data.json", "w") as f:
        json.dump(data, f)

def load_save():
    global User
    with open("data.json", "r") as f:
        data = json.load(f)
    name = data["name"]
    class_type = data["class_type"]
    lv = data["lv"]
    xp = data["xp"]
    hp = data["hp"]
    atk = data["atk"]
    df = data["df"]
    spd = data["spd"]
    abilities = data["abilities"]
    gold = data["gold"]
    upg_pts = data["upg_pts"]
    ready = data["ready"]
    User = Player(name, class_type, lv, xp, hp, atk, df, spd, abilities, gold, upg_pts, ready)

def start_tutorial():
    input("Welcome to Battle World!")
    input("Lets start with the basics.")
    input("You can fight monsters to gain experience and gold. Level up to become stronger!")
    input(f"Your current stats are:")
    time.sleep(1)
    show_stats()
    time.sleep(3)
    print("These are all the stats. If you're wondering, speed indicates how fast you can flee from a monster.")
    print("Now, lets get a monster to fight.")
    time.sleep(1)
    intro_monster = Monster(list(monsters.keys())[0], monsters["Goblin"]["lvl"], monsters["Goblin"]["xpdf"], monsters["Goblin"]["hp"], monsters["Goblin"]["atk"], monsters["Goblin"]["df"], monsters["Goblin"]["spd"], monsters["Goblin"]["abilities"], monsters["Goblin"]["abidropchance"], monsters["Goblin"]["g"])
    while True:
        battle(User.hp, User.atk, User.df, None, User.spd, intro_monster.hp, intro_monster.atk, intro_monster.df, intro_monster.abilities, intro_monster.name, intro_monster.lv, intro_monster.spd)
        if win:
            gain(intro_monster)
            input("You have completed the tutorial!")
            break
        else:
            input("You have failed the tutorial. Please try again.")


def gain(monster):
    monlv, xp_gain, gold_gain, abi, abichance = monster.die()
    User.gain(monlv, xp_gain, gold_gain, abi, abichance)

def lose():
    User.lose()
    
while True:
    if os.path.exists(savepath):
        load_save()
        if User.ready == False:
            start_tutorial()
            User.ready = True
            break
        else:
            print("Save loaded successfully!")
            break
    else:
        new_player()
        break

while User.ready == True:
    save()
    action = input("What do you want to do? 1. Adventure 2. Apply points 3. Shop 4. View stats 5. Songs: ")
    if action == "1":
        eligible_monsters = []
        for monster in monsters.keys():
            if monsters[monster]["lvl"] <= User.lv and monsters[monster]["lvh"] >= User.lv:
                eligible_monsters.append(monster)     
        monster_rand_num = random.randint(1, len(eligible_monsters))
        monster_chosen = eligible_monsters[monster_rand_num-1]
        monlv = random.randint(monsters[monster_chosen]["lvl"], monsters[monster_chosen]["lvh"])
        monlv = monlv - round(monsters[monster_chosen]["lvh"]/3) + User.lv
        if monlv < 1:
            monlv = 1
        mon_items = Monster(monster_chosen, monlv, monsters[monster_chosen]["xpdf"], monsters[monster_chosen]["hp"], monsters[monster_chosen]["atk"], monsters[monster_chosen]["df"], monsters[monster_chosen]["spd"], monsters[monster_chosen]["abilities"], monsters[monster_chosen]["abidropchance"], monsters[monster_chosen]["g"])
        print(User.abilities)
        battle(User.hp, User.atk, User.df, User.abilities, User.spd, mon_items.hp, mon_items.atk, mon_items.df, mon_items.abilities, mon_items.name, mon_items.lv, mon_items.spd)
        if win:
            gain(mon_items)
        elif not win:
            lose()
        else:
            pass
    elif action == "2":
        if User.upg_pts == 0:
            input("You don't have any upgrade points.")
        else:
            print("Apply Points")
            apply_points()
    elif action == "3":
        pass
    elif action == "4":
        print("Your stats:")
        time.sleep(1)
        show_stats()
        input("Press enter to exit... ")
    elif action == "5":
        choice_5 = input("Pick an option: 1. Play a song 2. Stop playing current song: ")
        if choice_5 == "1":
            for number, song in enumerate(songs, start=1):
                print(f"{number}. {song}")
                time.sleep(0.1)
            while True:
                songnum = int(input(f"Choose the number of the song you want to play: "))
                if songnum >= 1:
                    song_chosen = songs[songnum-1]
                    break
                else:
                    input("Please enter a valid number.")
            while True:
                songloopnum = int(input(f"Play how many times? For just one time, enter 1. "))
                if songloopnum >= 1:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(f"music/{song_chosen}.mp3")
                    pygame.mixer.music.play(loops=songloopnum)
                    input(f"Now playing {song_chosen}!")
                    break
                else:
                    input("Invalid amount. Please choose again.")
        elif choice_5 == "2":
            pygame.mixer.music.stop()
            input("Successfully stopped song")
        else:
            input("Please choose a valid option.")
