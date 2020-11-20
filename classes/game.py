import random
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def check_endgame(clan1, clan2):
    # Check for running or endgame:
    if len(clan1) == 0:
        print(bcolors.OKGREEN + "YOU WIN!" + bcolors.ENDC)
        return False

    elif len(clan2) == 0:
        print(bcolors.FAIL + "YOU LOSE!!" + bcolors.ENDC)
        return False

    else:
        return True


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.max_hp = hp
        self.max_mp = mp
        self.hp = hp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.actions = ["Attack", "Magic", "Items"]
        self.items = items

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n\n" + bcolors.BOLD + bcolors.HEADER + self.name + bcolors.ENDC)
        print("\n" + bcolors.OKBLUE + "   ACTIONS:" + bcolors.ENDC)
        for act in self.actions:
            print("       " + str(i) + ": ", act)
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "   TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                name = re.sub('[:]', '', enemy.name)
                print("\n\n      " + str(i) + ". " + bcolors.BOLD + bcolors.HEADER + name + bcolors.ENDC)
                i += 1

    def choose_magic(self):
        i = 1

        print("\n" + bcolors.OKBLUE + "   MAGIC:" + bcolors.ENDC)
        print("       0: To go back")
        for spell in self.magic:
            print("       " + str(i) + ": " + spell.get_name() + " (Cost is: " + str(spell.cost) + ")")
            i += 1
        print("\n" + "Your current MP is: " + bcolors.OKBLUE + str(self.mp) + bcolors.ENDC)

    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKGREEN + "   ITEMS:" + bcolors.ENDC)
        print("       0: To go back")
        for item in self.items:
            print("       " + str(i) + ": " + item["id"].get_name() + "(" + str(
                item["id"].get_descrioption()) + ")" + " quantaty: " + str(item["qnt"]))
            i += 1

    def heal(self, heal):
        self.hp += heal
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def get_stats(self):
        hpbar = ""
        mpbar = ""
        bar_ticks = (self.hp / self.max_hp) * 100 / 4
        mp_ticks = (self.mp / self.max_mp) * 100 / 10

        while bar_ticks > 0:
            hpbar += "█"
            bar_ticks -= 1
        while len(hpbar) < 25:
            hpbar += " "

        while mp_ticks > 0:
            mpbar += "█"
            mp_ticks -= 1
        while len(mpbar) < 10:
            mpbar += " "

        hp_string = (str(self.hp) + "/" + str(self.max_hp))
        mp_string = (str(self.mp) + "/" + str(self.max_mp))

        while len(hp_string) < 9:
            hp_string = " " + hp_string

        while len(mp_string) < 7:
            mp_string = " " + mp_string

        print("                      _________________________              __________ ")
        print(bcolors.BOLD + self.name + hp_string + "  " +
              bcolors.OKGREEN + "|" + hpbar + "|   " + bcolors.ENDC +
              mp_string + bcolors.OKBLUE +
              "  |" + mpbar + "|" + bcolors.ENDC)

    def get_enemy_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.max_hp) * 100 / 2

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = (str(self.hp) + "/" + str(self.max_hp))

        while len(hp_string) < 9:
            hp_string = " " + hp_string

        print("                      -------------------------------------------------- ")
        print(bcolors.BOLD + self.name + hp_string + "  " +
              bcolors.FAIL + "|" + hp_bar + "|   " + bcolors.ENDC)

    def is_dead(self):
        return self.hp == 0



