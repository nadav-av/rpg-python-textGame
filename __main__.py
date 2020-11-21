from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random
import re


running = True

# Create Magic:
fire = Spell("Fire", 50, 130, "black")
thunder = Spell("Thunder", 65, 180, "black")
blizzard = Spell("Blizzard", 100, 210, "black")
meteor = Spell("Meteor", 200, 400, "black")
quake = Spell("Quake", 65, 180, "black")

cure = Spell("Cure", 100, 100, "white")
revive = Spell("Revive", 200, 300, "white")

# Create Items:
potion = Item("Potion", "potion", "Heals 50 HP", 50)
high_potion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
super_potion = Item("S-Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elexir", "Fully restores HP/MP of one party member", 9999)
mega_elixer = Item("M-Elixer", "elixer", "Fully restores party`s HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


# Create Players:
player_magic = [fire, thunder, blizzard, meteor, cure, revive]
player1_items = [{"id": potion, "qnt": 5},
                 {"id": high_potion, "qnt": 5},
                 {"id": super_potion, "qnt": 5},
                 {"id": elixer, "qnt": 5},
                 {"id": mega_elixer, "qnt": 5},
                 {"id": grenade, "qnt": 5}]

player2_items = [{"id": potion, "qnt": 5},
                {"id": high_potion, "qnt": 5},
                {"id": super_potion, "qnt": 5},
                {"id": elixer, "qnt": 5},
                {"id": mega_elixer, "qnt": 5},
                {"id": grenade, "qnt": 5}]

player3_items = [{"id": potion, "qnt": 5},
                {"id": high_potion, "qnt": 5},
                {"id": super_potion, "qnt": 5},
                {"id": elixer, "qnt": 5},
                {"id": mega_elixer, "qnt": 5},
                {"id": grenade, "qnt": 5}]

player1 = Person("Aragon:   ", 4162, 88, 350, 34, player_magic, player1_items)
player2 = Person("Legolas:  ", 2400, 240, 152, 34, player_magic, player2_items)
player3 = Person("Gimli:    ", 3889, 112, 290, 34, player_magic, player3_items)

party = [player1, player2, player3]

enemy1 = Person("Joker:    ", 4162, 88, 350, 34, player_magic,  player1_items)
enemy2 = Person("Riddler:  ", 2400, 240, 152, 34, player_magic,  player2_items)
enemy3 = Person("Falcon:   ", 3889, 112, 290, 34, player_magic, player3_items)

enemies = [enemy1, enemy2, enemy3]

# Game begins:
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)


while running:

    print("=======================")

    # Status
    print("\n")
    print("NAME                 HP                                       MP")
    for player in party:
        player.get_stats()

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for i in party:
        i.mp += random.randrange(1,11)
        if i.mp > i.max_mp:
            i.mp = i.max_mp

    for player in party:
        # Player turn :
        player.choose_target(enemies)
        enm = int(input("\nChoose enemy: "))- 1
        player.choose_action()
        choice = input("\nChoose action: ")
        index = int(choice) - 1

        if choice == 0:
            continue

        # Attacking
        if index == 0:
            dmg = player.generate_damage()
            enemies[enm].take_dmg(dmg)
            print(bcolors.FAIL + "You attacked for: ", dmg, "points of damage" + bcolors.ENDC)
            for i in enemies:
                if i.get_hp() == 0:
                    print(i.name + "Is dead")
                    enemies.remove(i)

        # Spelling:
        elif index == 1:
            player.choose_magic()
            check = False
            magic_choice = int(input("\nChoose magic: ")) - 1
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            cost = spell.get_cost()

            while cost > player.get_mp():
                print("You don`t have enough mp")
                magic_choice = int(input("\nChoose other spell: ")) - 1
                if magic_choice == -1:
                    check = True
                    break
                spell = player.magic[magic_choice]
                cost = spell.get_cost()

            if check:
                continue

            player.reduce_mp(cost)
            magic_dmg = spell.generate_damage()

            if spell.var == "black":
                enemies[enm].take_dmg(magic_dmg)
                print(bcolors.FAIL + "\n" + spell.get_name() + " causes " + str(magic_dmg) + " points of damage " + bcolors.ENDC)
                for i in enemies:
                    if i.get_hp() == 0:
                        print(i.name + "Is dead")
                        enemies.remove(i)

            elif spell.var == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.get_name() + " heals for " + str(magic_dmg) + " HP" + bcolors.ENDC)

        # Item:
        elif index == 2:
            player.choose_item()
            item_choice = int(input("\nChoose item: ")) - 1
            item = player.items[item_choice]["id"]

            while player.items[item_choice]["qnt"] == 0:
                print("You don`t have any " + str(item.get_name()))
                item_choice = int(input("\nChoose other item: ")) - 1

            if item_choice == -1:
                continue

            player.items[item_choice]["qnt"] -= 1
            if item.var == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.get_name() + " heals for " + str(item.prop) + " HP" + bcolors.ENDC)
            elif item.var == "elixer":
                if item.name == "M-Elixer":
                    for i in party:
                        player.hp = player.max_hp
                        player.mp = player. max_mp
                else:
                    player.hp = player.max_hp
                    player.mp = player.max_mp
                print(bcolors.OKGREEN + "\n" + item.get_name() + "Fully restores HP/MP" + bcolors.ENDC)
            elif item.var == "attack":
                enemies[enm].take_dmg(item.id.prop)
                print(bcolors.FAIL + "\n" + item.get_name() + " causes " + str(item.prop) + " points of damage " + bcolors.ENDC)
                for i in enemies:
                    if i.get_hp() == 0:
                        print(i.name + "Is dead")
                        enemies.remove(i)



                # Check for running or endgame:
            if len(enemies) == 0:
                print(bcolors.OKGREEN + "YOU WIN!" + bcolors.ENDC)
                running = False
                break


    # Enemy turn :
    print("=======================" + "\n")
    if len(enemies) == 0:
        print(bcolors.OKGREEN + "YOU WIN!" + bcolors.ENDC)
        running = False
        break
    for enemy in enemies:
        target = random.randrange(0, 3)
        ename = re.sub('[:]', '', enemy.name)
        pname = re.sub('[:]', '', party[target].name)
        enemy_choice = random.randrange(0, 2)
        if enemy_choice == 0:
            enemy_dmg = enemy.generate_damage()
            party[target].take_dmg(enemy_dmg)
            print(bcolors.FAIL + ename.replace(" ", "") + " attacks " + pname.replace(" ", "") + " for: " + str(enemy_dmg) + bcolors.ENDC)
            if party[target].hp == 0:
                print(party[target].name + " Died ")
                party.remove(party[target])
            if len(party) == 0:
                print(bcolors.FAIL + "YOU LOSE!!" + bcolors.ENDC)
                running = False
                break

        elif enemy_choice == 1:
            magic_choice = random.randrange(0, len(enemy.magic))
            spell = enemy.magic[magic_choice]
            cost = spell.get_cost()
            while cost > enemy.get_mp():
                magic_choice = random.randrange(0, len(enemy.magic))
                spell = enemy.magic[magic_choice]
                cost = spell.get_cost()

            mag_dmg = spell.generate_damage()
            enemy.reduce_mp(cost)

            if spell.var == "white":
                enemy.heal(mag_dmg)
                print(bcolors.OKGREEN + "\n" + enemy.name + " heals for " + str(mag_dmg) + " HP" + bcolors.ENDC)
            if spell.var == "black":
                party[target].take_dmg(mag_dmg)
                print(bcolors.FAIL + ename.replace(" ", "") + " " + spell.name + " " + pname.replace(" ", "") + " for: " + str(
                    mag_dmg) + bcolors.ENDC)
                if party[target].hp == 0:
                    print(party[target].name + "Died")
                    party.remove(party[target])
                if len(party) == 0:
                    print(bcolors.FAIL + "YOU LOSE!!" + bcolors.ENDC)
                    running = False
                    break


