#! python3
# TextGames
# version 1.6.3
# description: scrambled saved game data, formatted save timestamp, added game loading instruction, tweaked file exceptions


# imports
import random
import datetime
import json
import base64


# functions
def locale(current_room):
    # rule for special that is displayed before room text
    if game_choice == '4' and current_room == 12:
        if room in special_rooms:
            do_special(room)

    print('You are ' + world[current_room]['prefix'] + ' ' + world[current_room]['name'] + world[current_room]['name2'] + '.')
    print(world[current_room]['desc'])

    if verbose_mode == True and locale_visited == False:
        show_exits(current_room)
    show_things(current_room)
    show_creatures(current_room)
    if room in special_rooms:
        do_special(room)


def look_around(current_room):
    global move
    global last_move

    print('You are ' + world[current_room]['prefix'] + ' ' + world[current_room]['name'] + world[current_room]['name2'] + '.')
    print(world[current_room]['desc'])
    show_exits(current_room)
    show_things(current_room)
    show_creatures(current_room)
    last_move = move

def examine_item(current_room):
    global inventory_quantity
    global room_has_items
    global room_has_mobs
    global target
    global move
    global last_move

    update_things_in_room(current_room)
    if target in available_targets(current_room):
        for thing in things:
            if thing['name'].lower() == target.lower():
                print(thing['description'])
                last_move = move + ' ' + target
                return

    if room_has_mobs:
        for mob in creatures:
            if mob['room'] == current_room and mob['name'].lower() == target:
                if mob['is_dead']:
                    print(mob['dead_description'])
                else:
                    print(
                        mob['description'] + '\n' + mob['name'] + ' ' + creature_wellness(mob['current_hp'], mob['max_hp']),
                        end='')
                    if mob['is_hostile']:
                        print(' ' + mob['status_hostile'])
                    else:
                        print(' ' + mob['status_neutral'])
                last_move = move
                return

    if room_has_items or inventory_quantity > 0 or room_has_mobs:
        available_choices = []
        print('Things you can examine:')
        if room_has_mobs:
            for mob in creatures:
                if mob['room'] == current_room:
                    print(mob['name'].capitalize())
                    available_choices.append(mob['name'].lower())
        if room_has_items:
            for thing in things:
                if thing['location'] == current_room and thing['on_person'] == False:
                    print(thing['name'].capitalize())
                    available_choices.append(thing['name'].lower())
        if inventory_quantity > 0:
            for thing in things:
                if thing['on_person'] == True:
                    print(thing['name'].capitalize())
                    available_choices.append(thing['name'].lower())
        print('What do you want to examine? (type the name or press ENTER for none)')
        choice = input('Examine: ').lower()
        if choice == '':
            return
        while choice not in available_choices:
            print('That\'s not a valid choice. Try again.')
            print('What do you want to examine? (type the name or press ENTER for none)')
            choice = input('Examine: ').lower()
            if choice == '':
                return
        for thing in things:
            if thing['name'].lower() == choice:
                print(thing['description'])
                last_move = move + ' ' + choice
        for mob in creatures:
            if mob['name'].lower() == choice:
                if mob['is_dead'] == True:
                    print(mob['dead_description'])
                else:
                    print(
                        mob['description'] + '\n' + mob['name'] + ' ' + creature_wellness(mob['current_hp'], mob['max_hp']),
                        end='')
                    if mob['is_hostile'] == False:
                        print(' ' + mob['status_neutral'])
                    else:
                        print(' ' + mob['status_hostile'])
                last_move = move + ' ' + choice
    else:
        print('There isn\'t anything to examine here. Go find something!')
        last_move =  ' ' + move


def creature_wellness(current, max):
    percentage = current / max * 100
    if percentage > 75:
        return "is in good shape." + " (" + str(current) + "/" + str(max) + ")"
    elif percentage > 50:
        return "appears to be in some pain." + " (" + str(current) + "/" + str(max) + ")"
    elif percentage > 25:
        return "is hurting but still dangerous." + " (" + str(current) + "/" + str(max) + ")"
    elif percentage > 0:
        return "is seriously wounded." + " (" + str(current) + "/" + str(max) + ")"
    else:
        return "is dead."


def show_creatures(current_room):
    global room_has_mobs
    room_has_mobs = False
    for mob in creatures:
        if mob['room'] == current_room:
            if not mob['is_dead']:
                if mob['is_hostile']:
                    print(mob['name'] + ' is here. ' + mob['status_hostile'])
                else:
                    print(mob['name'] + ' is here. ' + mob['status_neutral'])
                if not mob['was_seen']:
                    print(mob['description'] + '\n')
                    mob['was_seen'] = True
            else:
                print(mob['name'] + ' is here, but it\'s dead.')
            room_has_mobs = True


def show_things(current_room):
    global room_has_items
    visible_items = 0
    for thing in things:
        if thing['location'] == current_room and thing['on_person'] == False:
            visible_items = visible_items + 1
            room_has_items = True
    if visible_items == 0:
        # removed message about not seeing anything since some special events text contradicts. plus, it is superfluous
        #print('You don\'t see anything special.')
        room_has_items = False
    else:
        print('Visible items:')
        for thing in things:
            if thing['location'] == current_room and thing['on_person'] == False:
                print(thing['prefix'].capitalize() + ' ' + thing['name'])


def update_things_in_room(current_room):
    global room_has_items
    global room_has_mobs
    visible_items = 0
    for thing in things:
        if thing['location'] == current_room and thing['on_person'] == False:
            visible_items = visible_items + 1
            room_has_items = True
    if room_has_mobs:
        for mob in creatures:
            if mob['room'] == current_room and mob['name'].lower() == target:
                visible_items = visible_items + 1
                room_has_items = True

    if visible_items == 0:
        room_has_items = False


def show_inventory(quantity):
    global move
    global last_move

    if quantity > 0:
        print('You are carrying:')
        for thing in things:
            if thing['on_person'] == True:
                print(thing['prefix'].capitalize() + ' ' + thing['name'])
    else:
        print('You aren\'t carrying anything.')
    last_move = move


def take_item(current_room):
    global inventory_quantity
    global room_has_items
    global target
    global move
    global last_move
    update_things_in_room(current_room)

    if room_has_items:
        available_choices = []
        for thing in things:
            if thing['location'] == current_room and thing['on_person'] == False:
                available_choices.append(thing['name'].lower())
        for thing in things:
            if thing['name'].lower() == target.lower():
                if thing['on_person'] == True:
                    print('You already have the ' + thing['name'] + '.')
                    last_move = move + ' ' + target
                    return
                if thing['moveable'] == True and thing['location'] == current_room:
                    thing['on_person'] = True
                    inventory_quantity = inventory_quantity + 1
                    # old print('You pick up ' + thing['prefix'] + ' ' + thing['name'] + '.')
                    print('You pick up the ' + thing['name'] + '.')
                    last_move = move + ' ' + target
                    return
                else:
                    # old print('You can\'t take ' + thing['prefix'] + ' ' + thing['name'] + '.')
                    if thing['location'] != current_room:
                        print('What ' + thing['name'] + '?')
                    else:
                        print('You can\'t take the ' + thing['name'] + '.')
                    return

        print('Items you see:')
        for thing in range(len(available_choices)):
            print(available_choices[thing].capitalize())
        print('What item do you want to take? (type the item name or press ENTER for none)')
        choice = input('Take: ').lower()
        if choice == '':
            return
        while choice not in available_choices:
            print('That\'s not a valid choice. Try again.')
            print('What item do you want to take? (type the item name or press ENTER for none)')
            choice = input('Take: ').lower()
            if choice == '':
                return
        for thing in things:
            if thing['name'].lower() == choice:
                if thing['moveable'] == True:
                    thing['on_person'] = True
                    inventory_quantity = inventory_quantity + 1
                    print('You pick up the ' + thing['name'] + '.')
                    last_move = move + ' ' + choice
                    # old print('You pick up ' + thing['prefix'] + ' ' + thing['name'] + '.')
                else:
                    print('You can\'t take the ' + thing['name'] + '.')
                    last_move = move + ' ' + choice
                    # old print('You can\'t take ' + thing['prefix'] + ' ' + thing['name'] + '.')
    else:
        for thing in things:
            if thing['name'].lower() == target.lower():
                if thing['on_person'] == True:
                    print('You already have the ' + thing['name'] + '.')
                    last_move = move + ' ' + target
                    return
        print('There aren\'t any items worth taking.')


def drop_item(current_room):
    global inventory_quantity
    global target
    global move
    global last_move

    if inventory_quantity == 0:
        print('You aren\'t carrying anything.')
        return

    update_things_in_room(current_room)
    if target != '':
        if target in available_targets(current_room):
            for thing in things:
                if thing['name'].lower() == target.lower():
                    if thing['on_person'] == False:
                        print('You aren\'t carrying the ' + thing['name'] + '.')
                    else:
                        if thing['no_drop'] == True:
                            print('You can\'t drop the ' + thing['name'] + '.')
                        else:
                            thing['on_person'] = False
                            thing['location'] = current_room
                            user_has_items = True
                            print('You drop the ' + thing['name'] + '.')
                            # old print('You drop ' + thing['prefix'] + ' ' + thing['name'] + '.')
                            inventory_quantity = inventory_quantity - 1
            last_move = move + ' ' + target
            return
        else:
            print('\"' + target + '\" is not in your inventory.')
            last_move = move + ' ' + target

    if inventory_quantity > 0:
        available_choices = []
        print('Items you are carrying:')
        for thing in things:
            if thing['on_person'] == True:
                print(thing['name'].capitalize())
                available_choices.append(thing['name'].lower())
        print('What item do you want to drop? (type the item name or press ENTER for none)')
        choice = input('Drop: ').lower()
        if choice == '':
            return
        while choice not in available_choices:
            print('That\'s not a valid choice. Try again.')
            print('What item do you want to drop? (type the item name or press ENTER for none)')
            choice = input('Drop: ').lower()
            if choice == '':
                return
        for thing in things:
            if thing['name'].lower() == choice:
                if thing['no_drop'] == True:
                    print('You can\'t drop the ' + thing['name'] + '.')
                else:
                    thing['on_person'] = False
                    thing['location'] = current_room
                    user_has_items = True
                    print('You drop the ' + thing['name'] + '.')
                    # old print('You drop ' + thing['prefix'] + ' ' + thing['name'] + '.')
                    inventory_quantity = inventory_quantity - 1
                    last_move = move + ' ' + choice
    else:
        print('You aren\'t carrying anything.')
        last_move = move


def use_item(current_room):
    global inventory_quantity
    global room_has_items
    global target
    global move
    global last_move

    update_things_in_room(current_room)
    if target != '':
        if target in available_targets(current_room):
            if weapon_checker(target) == True:
                if defense_checker(target) == True:
                    if random.randrange(2) == 0:
                        print('You hide in your shell.')
                    else:
                        check_event(current_room, target)
                else:
                    pick_up_if_weapon(target)
                    if attack_checker(current_room):
                        check_event(current_room, target)
                        player_attack(current_room, target)
                    else:
                        check_event(current_room, target)
            else:
                check_event(current_room, target)
            if defense_checker(target) == True:
                creature_attack_block(current_room)
            else:
                creature_attack(current_room)
            last_move = move + ' ' + target
            return
        else:
            print('\"' + target + '\" is not available to use.')

    if room_has_items or inventory_quantity > 0:
        available_choices = []
        print('Items you can use:')
        if room_has_items:
            for thing in things:
                if thing['location'] == current_room and thing['on_person'] == False:
                    print(thing['name'].capitalize())
                    available_choices.append(thing['name'].lower())
        if inventory_quantity > 0:
            for thing in things:
                if thing['on_person'] == True:
                    print(thing['name'].capitalize())
                    available_choices.append(thing['name'].lower())
        print('What item do you want to use? (type the item name or press ENTER for none)')
        choice = input('Use: ').lower()
        if choice == '':
            return
        while choice not in available_choices:
            print('That\'s not a valid choice. Try again.')
            print('What item do you want to use? (type the item name or press ENTER for none)')
            choice = input('Use: ').lower()
            if choice == '':
                return

        if weapon_checker(choice) == True:
            if defense_checker(choice) == True:
                if random.randrange(2) == 0:
                    print('You hide in your shell.')
                else:
                    check_event(current_room, choice)
            else:
                pick_up_if_weapon(choice)
                if attack_checker(current_room):
                    check_event(current_room, choice)
                    player_attack(current_room, choice)
                else:
                    check_event(current_room, choice)
        else:
            check_event(current_room, choice)
        if defense_checker(choice) == True:
            creature_attack_block(current_room)
        else:
            creature_attack(current_room)
        last_move = move + ' ' + choice
    else:
        print('There isn\'t anything you can use here.')


def attack_checker(current_room):
    global room_has_mobs

    if room_has_mobs:
        for mob in creatures:
            if mob['room'] == current_room and mob['is_dead'] == False:
                if mob['is_hostile'] == False:
                    print('Do you want to attack ' + mob['name'] + '? This will make it hostile towards you.')
                    fight = input('Enter \'Y\' or \'Yes\': ')
                    if fight.lower() == 'y' or fight.lower() == 'yes':
                        return True
                    else:
                        return False
                else:
                    return True  ## assumes once mob is hostile that player wants to fight it


def player_attack(current_room, weapon):
    global room_has_mobs

    if room_has_mobs:
        for mob in creatures:
            if mob['room'] == current_room and mob['is_dead'] == False:
                for thing in things:
                    if thing['name'].lower() == weapon and thing['is_weapon'] == False:
                        return
                    mob['is_hostile'] = True
                    if current_room in special_rooms:
                        do_special(current_room)

                    # debug print(weapon)
                    # debug print('hit_bonus: ' + str(thing['hit_bonus']) + ' damage: '+ str(thing['damage']))
                    if (random.randrange(0, 100) + thing['hit_bonus']) > 50:
                        damage = thing['base_damage'] + random.randrange(0, (thing['damage'] + 1))
                        if weapon[-1] == 's':
                            print('They hit ' + mob['name'] + ' for ' + str(damage) + ' damage.')
                        else:
                            print('It hits ' + mob['name'] + ' for ' + str(damage) + ' damage.')
                        mob['current_hp'] = mob['current_hp'] - damage
                        if mob['current_hp'] <= 0:
                            print('That was a fatal blow.')
                            mob['is_dead'] = True

                    else:
                        miss = random.randrange(1, 11)
                        if miss < 6:
                            if weapon[-1] == 's':
                                print('They miss ' + mob['name'] + '.')
                            else:
                                print('It misses ' + mob['name'] + '.')
                        elif miss < 9:
                            print(mob['name'] + ' dodges the attack.')
                        else:
                            print('The attack glances off ' + mob['name'] + '.')

                    print(mob['name'] + ' ' + creature_wellness(mob['current_hp'], mob['max_hp']) )
                    if mob['is_dead'] == True:
                        if mob['death_event'] != 0:
                            do_event(mob['death_event'], current_room)
                        return
                    else:
                        print('')
                        return


def creature_attack(current_room):
    global room_has_mobs
    global player_hp

    if room_has_mobs:
        for mob in creatures:
            if mob['room'] == current_room and mob['is_dead'] == False and mob['is_hostile'] == True:
                if mob['is_fatigued'] == False and mob['attack_chance'] >= random.randrange(1, 101):
                    print(mob['name'] + ' attacks!')
                    mob['is_fatigued'] = True
                    if (random.randrange(1, 101) + mob['hit_bonus']) > 50:
                        #damage = 5 # for testing
                        #print('NERFED! It hits you for ' + str(damage) + ' damage.') # for testing
                        damage = 10 + random.randrange(0, (mob['damage'] + 1))
                        print('It hits you for ' + str(damage) + ' damage.')
                        player_hp = player_hp - damage
                        if player_hp <= 0:
                            print('That was a fatal blow.')
                    else:
                        miss = random.randrange(1, 11)
                        if miss < 6:
                            print('It misses you.')
                        elif miss < 9:
                            print('You dodge the attack.')
                        else:
                            print('The attack glances off you.')
                else:
                    hostile_posture = random.randrange(1, 4)
                    if hostile_posture == 1:
                        print(mob['name'] + ' gives you a hateful stare.')
                    elif hostile_posture == 2:
                        print(mob['name'] + ' catches its breath.')
                    else:
                        print(mob['name'] + ' readies for combat.')

                player_wellness(player_hp, 100)


def creature_attack_block(current_room):
    global room_has_mobs
    global player_hp

    if room_has_mobs:
        for mob in creatures:
            if mob['room'] == current_room and mob['is_dead'] == False and mob['is_hostile'] == True:
                if mob['is_fatigued'] == False and mob['attack_chance'] >= random.randrange(1, 101):
                    print('\n' + mob['name'] + ' attacks!')
                    mob['is_fatigued'] = True
                    if (random.randrange(1, 101) + mob['hit_bonus']) > 50:
                        block_type = random.randrange(1,101)
                        if block_type <= 25: # complete block
                            print('Your shell blocks all damage.')
                        elif block_type <= 50: # damage converted to health
                            print('Your shell absorbs the attack and converts part of it into health.')
                            player_hp = player_hp + random.randrange(1, 4)
                            if player_hp > 100:
                                player_hp = 100
                        elif block_type <= 75: # damage lessened
                            print('The assault is partly lessened by your shell.')
                            damage = int((6 + random.randrange(0, (mob['damage'] + 1))) / 2)
                            print('It hits you for ' + str(damage) + ' damage.')
                            player_hp = player_hp - damage
                            if player_hp <= 0:
                                print('That was a fatal blow.')
                        else: # damage reflected onto attacker
                            print('Your shell deflects the attack back onto your enemy.')
                            damage = int((10 + random.randrange(0, (mob['damage'] + 1))) / 4)
                            print('It hits ' + mob['name'] + ' for ' + str(damage) + ' damage.')
                            mob['current_hp'] = mob['current_hp'] - damage
                            if mob['current_hp'] <= 0:
                                print('That was a fatal blow.')
                                mob['is_dead'] = True
                            print(mob['name'] + ' ' + creature_wellness(mob['current_hp'], mob['max_hp']))
                            if mob['is_dead'] == True:
                                if mob['death_event'] != 0:
                                    do_event(mob['death_event'], current_room)
                                # return
                            else:
                                print('')
                                # return
                    else:
                        miss = random.randrange(1, 11)
                        if miss < 6:
                            print('It misses you.')
                        elif miss < 9:
                            print('You dodge the attack.')
                        else:
                            print('The attack glances off you.')
                else:
                    hostile_posture = random.randrange(1, 4)
                    if hostile_posture == 1:
                        print(mob['name'] + ' gives you a hateful stare.')
                    elif hostile_posture == 2:
                        print(mob['name'] + ' catches its breath.')
                    else:
                        print(mob['name'] + ' readies for combat.')

                if mob['is_dead'] == False:
                    player_wellness(player_hp, 100)


def creature_follow(current_room, new_room):
    global room_has_mobs
    global player_hp
    global exit_room
    global safe_rooms

    if new_room in safe_rooms:
        return

    if new_room == exit_room:
        return

    if room_has_mobs:
        for mob in creatures:
            if mob['room'] == current_room and mob['is_dead'] == False and mob['is_hostile'] == True:
                mob['room'] = new_room
                print(mob['name'] + ' follows you.')


def remove_creature_fatigue(current_room):
    global room_has_mobs

    if room_has_mobs:
        for mob in creatures:
            if mob['room'] == current_room and mob['is_dead'] == False and mob['is_hostile'] == True:
                mob['is_fatigued'] = False


def player_wellness(current, max):
    global move
    global last_move

    percentage = current / max * 100
    if percentage > 75:
        print("You are in good shape. (" + str(current) + "/" + str(max) + ')')
    elif percentage > 50:
        print("You are in some pain. (" + str(current) + "/" + str(max) + ')')
    elif percentage > 25:
        print("You are hurting but still able to fight. (" + str(current) + "/" + str(max) + ')')
    elif percentage > 0:
        print("You are seriously wounded. (" + str(current) + "/" + str(max) + ')')
    else:
        print("You are dead.")
    last_move = move


def weapon_checker(item):
    global inventory_quantity
    for thing in things:
        if thing['name'].lower() == item:
            if thing['is_weapon']:
                return True
            else:
                return False

def defense_checker(item):
    global inventory_quantity

    if game_choice == '4':
        if item.lower() == 'shell':
             return True
        else:
            return False
    else:
        return False


def pick_up_if_weapon(item):
    global inventory_quantity
    for thing in things:
        if thing['name'].lower() == item and thing['is_weapon'] == True:
            if thing['on_person']:
                return
            thing['on_person'] = True
            inventory_quantity = inventory_quantity + 1
            print('You pick up the ' + thing['name'] + '.')


def available_targets(current_room):
    global inventory_quantity
    global room_has_items
    global target
    update_things_in_room(current_room)
    available_choices = []
    if room_has_items or inventory_quantity > 0:
        if room_has_items:
            for thing in things:
                if thing['location'] == current_room and thing['on_person'] == False:
                    available_choices.append(thing['name'].lower())
        if inventory_quantity > 0:
            for thing in things:
                if thing['on_person']:
                    available_choices.append(thing['name'].lower())
    return available_choices


def check_event(current_room, used_item):
    # print('DEBUG: checking what happens when using ' + used_item + ' in room # ' + str(current_room))
    # print(events)
    for event in events:
        if event['room'] == current_room and event['item_name'].lower() == used_item:
            if not event['done']:
                do_event(event['id'], current_room)
                return
            else:
                print(event['already_done_text'])
                return
        # problem if item can be used in 999 and in specific room - solution? make event index of specific room event lower than event index of any room 999? or have specific room inserted before 999?
        if event['room'] == 999 and event['item_name'].lower() == used_item:
            if not event['done']:
                do_event(event['id'], current_room)
                return
            else:
                print(event['already_done_text'])
                return
    print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')


def do_multi_step_event(event_id):
    global game_choice

    if game_choice == '4':
        if event_id in [6, 7, 8]:
            shell_list = [events[6]['done'], events[7]['done'], events[8]['done'] ]
            if all(shell_list):
                print('This time a loud creaking noise rumbles through the water. Something has changed somewhere.')
                # new room becomes visible
                world[36]['visible'] = True
                # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
                world[17][
                    'desc'] = 'Tall reeds are thick in the northern edge of the lake. As you swim through the water, you see the surface above. The massive clam shell has opened revealing a passage to the north. The shallows extend to the east and to the west. Another cave entrance lies below.'
                # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
                world[17]['exits'] = {'n': 36, 'e': 16, 'w': 18, 'd': 25}
                delete_thing('clam shell')

            elif shell_list.count(True) == 2:
                print('A short, grinding sound is heard from elsewhere in the lake. You start to sense a pattern.')
            else:
                print('You hear a dull click in the distance.')

def do_event(event_id, current_room):
    global inventory_quantity
    global game_choice
    global player_hp
    global room

    if game_choice == '1':

        # simple event: print text only
        # mona lisa wink, ball in house x 3, ride trike, ball everywhere besides house, post, machine, broken well
        if event_id in [0, 1, 4, 8, 9, 10, 12, 13, 14, 15, 16]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True

        # create room event template
        # plant tree
        if event_id in [2]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # new room
            world[7]['visible'] = True
            # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
            world[4][
                'desc'] = 'The grassy clearing at the end of the road is accented by a few tall trees. A new tree in the center has low, inviting branches. Part of the grass is bare along the southern edge, and it contains a strange etching of a house and a winged creature. The street is at the north end of the park, a trail leads through the trees to the west, and a meadow is to the east.'
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[4]['exits'] = {'n': 3, 'u': 7, 'e': 10, 'w': 11}
            # find item and modify description
            item_index = ['tree kit' in i['name'] for i in things].index(True)
            things[item_index][
                'description'] = 'The empty tree kit box claims: \'Makes a real life tree in seconds! No digging required. For best results, use in an open area.\''
        # create portal
        if event_id in [7]:
            # birdhouse is prerequisite - if 'birdhouse' required because using robin in yard only has effect if birdhouse has been created
            if 'birdhouse' in str(things):
                print(events[event_id]['first_time_text'])
                events[event_id]['done'] = True
                # new room
                world[5]['visible'] = True
                # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
                world[4][
                    'desc'] = 'The grassy clearing at the end of the road is dappled with light shining through the tall trees. A new tree in the center has low, inviting branches. Where the grass was worn to the south, you now see a brightly glowing portal! The street is at the north end of the park, a trail leads through the trees to the west, and a meadow is to the east.'
                # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
                world[4]['exits'] = {'n': 3, 'u': 7, 's': 5}
                delete_thing('robin')
                # removing this since delete_thing adjusts inventory        inventory_quantity = inventory_quantity - 1
            else:
                print('Nothing happened.')
        # unlock gate
        if event_id in [20]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # new room
            world[13]['visible'] = True
            # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
            world[12][
                'desc'] = 'This gentle valley is surrounded by leafy trees and bushes. A path is visible to the west. To the north you see an open iron gate, beyond which lies the mouth of a cave.'
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[12]['exits'] = {'e': 11, 'n': 13}

        # create thing event template
        # remove bird from egg
        if event_id in [3]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'robin', 'prefix': 'a',
                           'description': 'Its feathers are matted down by egg goo, and the baby bird is struggling to open its tiny eyes. It would be gross if it weren\'t so darn cute.',
                           'location': 7, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False})
            inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
            things.append({'name': 'egg shell', 'prefix': 'an',
                           'description': 'There\'s little to do with the broken egg shell shards.', 'location': 7,
                           'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
            delete_thing('egg')
        # reveal basement
        if event_id in [5]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'toy house', 'prefix': 'a',
                           'description': 'This miniature colonial appears to be worn from play. You can imagine dolls going in and out of the doors and windows.',
                           'location': 6, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        # make birdhouse
        if event_id in [6]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'birdhouse', 'prefix': 'a',
                           'description': 'The toy house resting atop the post will surely attract small, avian creatures.',
                           'location': 1, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False})
            delete_thing('toy house')
        # make flashlight
        if event_id in [11]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'flashlight', 'prefix': 'a',
                           'description': 'It\'s your standard issue flashlight. Looks like it could help you see in dark places, but it wouldn\'t do much elsewhere.',
                           'location': 9, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
            delete_thing('coin')
        # make functional well
        if event_id in [17]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'well', 'prefix': 'the',
                           'description': 'The well is still old, but now you can raise and lower the bucket.',
                           'location': 10, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False})
            delete_thing('broken well')
            delete_thing('bucket')
        # make key
        if event_id in [18]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'key', 'prefix': 'a',
                           'description': 'The brass key is partially covered in moss. It feels heavy.', 'location': 10,
                           'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        # drop pebble
        if event_id in [19]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            delete_thing('pebble')

    elif game_choice == '2':
        if event_id in [0]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
        if event_id in [1]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            player_hp = player_hp + 50
            if player_hp > 100:
                player_hp = 100
            ###  player_wellness(player_hp, 100)   removing this because it can be redundant
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'empty bottle', 'prefix': 'an',
                           'description': 'Staring at the empty elixir bottle fills you with longing.', 'location': 1,
                           'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False})
            inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
            delete_thing('elixir')
        # magic key drops from monster upon death
        if event_id in [3]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM OR USE current_room VARIABLE
            things.append({'name': 'magic key', 'prefix': 'a',
                           'description': 'The over-sized key is made of dark metal. It gives off a faint vibration.',
                           'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        # unlock grate
        if event_id in [2]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # new room
            world[2]['visible'] = True
            # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
            world[1][
                'desc'] = 'Packed dirt covers the floor of this spacious arena. A door is in the northwest corner. On the south wall, the words "EXIT BELOW" are painted in what could be dried blood. Or maybe ketchup? Below it is a large pit. You could probably climb down into it.'
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[1]['exits'] = {'nw': 0, 'd': 2}
            delete_thing('locked grate')

    elif game_choice == '3':

        global launch_code

        # simple event: print text only, put weapons in here
        if event_id in [0, 5, 6, 7, 10, 14, 16, 18, 19, 22, 27, 36, 37, 38, 41, 44, 45, 46]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
        # use stimpack
        if event_id in [1]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            player_hp = player_hp + 30
            if player_hp > 100:
                player_hp = 100
            things.append({'name': 'empty stimpack', 'prefix': 'an',
                           'description': 'The hollow tube of the used stimpack is of little use now.', 'location': current_room,
                           'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False})
            inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
            delete_thing('stimpack')
        # unlock detention elevator
        if event_id in [2]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # new room
            world[5]['visible'] = True
            # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
            world[4][
                'desc'] = 'The elevator goes up to the Main Deck. The detention hallway is to the east.'
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[4]['exits'] = {'e': 1, 'u': 5}
            delete_thing('keycard')
        # detention key card drops from guard upon death
        if event_id in [3]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM OR USE current_room VARIABLE
            things.append({'name': 'keycard', 'prefix': 'a',
                           'description': 'This sleek card reads, "Detention Elevator." Emblazoned under the text is an image of a box with an arrow inside it.',
                           'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        # using breathing mask
        if event_id in [4]:
            print(events[event_id]['first_time_text'])
            #events[event_id]['done'] = True  always do the first time text then add to inventory if not already there
            for thing in things:
                if thing['name'].lower() == 'breathing mask':
                    if thing['on_person']:
                        return
                    thing['on_person'] = True
                    inventory_quantity = inventory_quantity + 1
                    #print('You pick up the ' + thing['name'] + '.') first_time_text implies item is picked up
        # create empty fuel cell and quarters keycard
        if event_id in [8]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            delete_thing('fuel cell')
            delete_thing('corpse')
            things.append({'name': 'empty fuel cell', 'prefix': 'an',
                           'description': 'The spent fuel cell has nothing inside it.', 'location': 10,
                           'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False})
            inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'quarters keycard', 'prefix': 'a',
                           'description': 'After wiping it clean, you see this keycard has the words \'Crew Quarters\' printed on it.',
                           'location': 10, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        # unlock quarters elevator
        if event_id in [9]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # new room
            world[28]['visible'] = True
            # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
            world[13][
                'desc'] = 'The elevator goes down to Crew Quarters. To the east is a widening hallway.'
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[13]['exits'] = {'e': 12, 'd': 28}
            delete_thing('quarters keycard')
        # unlock mess elevator
        if event_id in [11]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # new room
            world[35]['visible'] = True
            # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
            world[34][
                'desc'] = 'This elevator goes down to the Mess Hall and Medical Services Deck. The observation deck is to the north.'
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[34]['exits'] = {'d': 35, 'n': 32}
            delete_thing('mess keycard')
        # detention key card drops from guard upon death
        if event_id in [12]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM OR USE current_room VARIABLE
            things.append({'name': 'mess keycard', 'prefix': 'a',
                           'description': 'This worn card reads, "Mess & Medical Elevator." Emblazoned under the text is an image of a box with an arrow inside it.',
                           'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        if event_id in [13]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'soldier eye', 'prefix': 'a',
                           'description': 'You don\'t feel great about how you got it, but the eyeball is pretty cool.',
                           'location': 39, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False})
            inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
            # replace existing soldier with a modified version
            delete_thing('fallen soldier')
            things.append({'name': 'fallen soldier', 'prefix': 'a',
                            'description': 'This dead crewmate is bent backwards, leaning on the countertop. They have the insignia and fatigues of a tactical combat specialist. '
                            'Unlike the other bodies you encountered, this one seems frozen in shock, face up with one eye and mouth wide open.',
                            'location': 39, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        # use large stimpack
        if event_id in [15]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            player_hp = player_hp + 90
            if player_hp > 100:
                player_hp = 100
            things.append({'name': 'empty large stimpack', 'prefix': 'an',
                           'description': 'There\'s not much to do with the large stimpack now that it is drained.', 'location': current_room,
                           'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False})
            inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
            delete_thing('large stimpack')
        # unlock armory elevator
        if event_id in [17]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # new room
            world[23]['visible'] = True
            # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
            world[11][
                'desc'] = 'The elevator goes down to the Armory. The wide hallway is to the north.'
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[11]['exits'] = {'n': 10, 'd': 23}
            events[38]['done'] = False

        # unlock bridge elevator
        if event_id in [20]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # new room
            world[42]['visible'] = True
            # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
            world[33][
                'desc'] = 'The elevator goes up to the Bridge. To the south is the observation deck.'
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[33]['exits'] = {'s': 32, 'u': 42}
            delete_thing('bridge keycard')
        # detention key card drops from guard upon death
        if event_id in [21]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM OR USE current_room VARIABLE
            things.append({'name': 'bridge keycard', 'prefix': 'a',
                           'description': 'This dark gray card has no words on it, but when held at a certain angle, a stylized bridge materialzes. Below the bridge image you can see a box with an arrow inside it.',
                           'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        # use wound salve
        if event_id in [23]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            player_hp = player_hp + 35
            if player_hp > 100:
                player_hp = 100
            things.append({'name': 'used wound salve', 'prefix': 'a',
                           'description': 'The wound salve jar is empty. What a shame.', 'location': current_room,
                           'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False})
            inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
            delete_thing('wound salve')
        # use hot sauce on hulking guard
        if event_id in [24]:
            if creature_in_same_room(current_room, 2):
                print(events[event_id]['first_time_text'])
                events[event_id]['done'] = True
                creatures[2]['current_hp'] = int(creatures[2]['current_hp'] * 0.75)
                delete_thing('hot sauce')
            else:
                print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')
        # use mayonnaise on hulking guard
        if event_id in [25]:
            if creature_in_same_room(current_room, 2):
                print(events[event_id]['first_time_text'])
                events[event_id]['done'] = True
                creatures[2]['current_hp'] = int(creatures[2]['current_hp'] * 0.75)
                delete_thing('mayonnaise')
            else:
                print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')
        # use pear powder on hulking guard
        if event_id in [26]:
            if creature_in_same_room(current_room, 2):
                print(events[event_id]['first_time_text'])
                events[event_id]['done'] = True
                creatures[2]['current_hp'] = int(creatures[2]['current_hp'] * 0.75)
                delete_thing('pear powder')
            else:
                print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')
        # assemble override lever from 3 parts
        if event_id in [28, 29, 30]:
            necessary_parts = 0
            for thing in things:
                if thing['name'] == 'allen claw' and ( thing['location'] == current_room or thing['on_person'] == True ):
                    necessary_parts += 1
                if thing['name'] == 'smooth bar' and ( thing['location'] == current_room or thing['on_person'] == True ):
                    necessary_parts += 1
                if thing['name'] == 'gummy grip' and ( thing['location'] == current_room or thing['on_person'] == True ):
                    necessary_parts += 1
            if necessary_parts == 3:
                things.append({'name': 'override lever', 'prefix': 'the',
                               'description': 'This majestic implement is full of potential. A genuine lever of power.',
                               'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
                inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
                delete_thing('allen claw')
                delete_thing('smooth bar')
                delete_thing('gummy grip')
                print(events[event_id]['first_time_text'])
            else:
                print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')
        # open bridge door
        if event_id in [31]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # new room
            world[44]['visible'] = True
            # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
            world[43][
                'desc'] = 'This is the bridge-level security desk. An open door to the bridge is to the west. To the east is the Systems Control room. South is an elevator bay.'
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[43]['exits'] = {'w': 44, 'e': 45, 's': 42}
        # use escape pod launch code generator
        if event_id in [32]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            launch_code = str(random.randrange(0, 10)) + str(random.randrange(0, 10)) + 'L07A' + str(random.randrange(0, 10)) + str(random.randrange(0, 10))
            print('It reads: ' + launch_code)
        # activate hangar elevator
        if event_id in [33]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # new room
            world[19]['visible'] = True
            # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
            world[9][
                'desc'] = 'The elevator goes down to the Hangar. To the south is the walkway.'
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[9]['exits'] = {'s': 8, 'd': 19}
            # remove old console create new one
            delete_thing('lockdown console')
            things.append({'name': 'lockdown console', 'prefix': 'the',
                       'description': 'The lockdown console has a small screen that reads: \n\t"NO LOCKDOWN - Offline systems: none"'
                                      '\nThere is an empty lever socket just below the screen.',
                       'location': 45, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        # use escape pod launch controls
        if event_id in [34]:
            print(events[event_id]['first_time_text'])
            code_checker()
        # use escape pod launch console
        if event_id in [35]:
            print(events[event_id]['first_time_text'])
            code_checker()
        # apply phaser booster
        if event_id in[39]:
            print(events[event_id]['first_time_text'])
            delete_thing('phaser')
            delete_thing('phaser booster')
            things.append({'name': 'phaser', 'prefix': 'a',
                       'description': 'The V-8 phaser pistol is a reliable mid- to close-range weapon, especially now that it is BOOSTED.',
                       'location': 999, 'on_person': True, 'moveable': True, 'is_weapon': True, 'base_damage': 25, 'damage': 30, 'hit_bonus': 45, 'no_drop': False})
            inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
        # use stimpack
        if event_id in [40]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            player_hp = player_hp + 60
            if player_hp > 100:
                player_hp = 100
            things.append({'name': 'empty medium stimpack', 'prefix': 'an',
                           'description': 'The medium stimpack served its purpose.', 'location': current_room,
                           'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False})
            inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
            delete_thing('medium stimpack')
        # unclog toilet and create metal key
        if event_id in [42]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM OR USE current_room VARIABLE
            things.append({'name': 'metal key', 'prefix': 'a', 'description': 'This small, silvery key has all the notches and grooves you expect to see in something that could unlock a door.',
                           'location': 47, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0, 'no_drop': False})
            # remove old toilet create new one
            delete_thing('clogged toilet')
            things.append({'name': 'toilet', 'prefix': 'a',
                           'description': 'The flush mechanism still doesn\'t work, but at least it is empty.',
                           'location': 47, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
                           'hit_bonus': 0, 'no_drop': False})
        # unlock workroom
        if event_id in [43]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # new room
            world[49]['visible'] = True
            # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
            world[48]['desc'] = 'This dingy space contains an array of maintenance tools and equipment. To the northeast is the Funneling hallway. On the west side of the room is a door to the Workroom. '
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[48]['exits'] = {'ne': 12, 'w': 49}

    elif game_choice == '4':
        # make updated faucet
        # simple event: print text only, put weapons in here
        if event_id in [5, 18, 22, 23, 24, 25, 26, 27, 28, 29, 30]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
        # add filter to sink
        if event_id in [0]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'enhanced faucet', 'prefix': 'an',
                           'description': 'The kitchen sink is now fitted with a gleaming filter. The water appears to clarify everything it touches.',
                           'location': 3, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False})
            delete_thing('filter')
            delete_thing('kitchen sink')
        # use faded note with upgraded faucet to reveal note and open front door
        if event_id in [1]:
            item_index = ['faded note' in i['name'] for i in things].index(True)
            if things[item_index]['on_person'] == True or things[item_index]['location'] == 3:
                print(events[event_id]['first_time_text'])
                events[event_id]['done'] = True
                # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
                things.append({'name': 'note', 'prefix': 'the',
                               'description': 'After rinsing the faded note in the filtered water, the text becomes sharper and more words are visible! It now reads:\n\n\t\'Our lake has been overtaken by a venomous tyrant.\n\t This creature of the sea has corrupted the waters and installed three hidden guardians.\n\t Only the one who wears the ring of power may enter the lake and save it.\n\t The one who bears symbols of great warriors can forge the ring at the water\'s edge.\n\t Peril now fills the lake. If you can emerge, even for a moment, you may find relief, or more danger.\n\t Find the guardians, remove them, and face the usurper. Purge this being from the lake to redeem it.\'',
                               'location': 3, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': True})
                inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
                delete_thing('faded note')
                world[9]['visible'] = True
                # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
                world[0][
                    'desc'] = 'This entryway is just inside the front door of your home. Most of the house is accessible from here. The dining room lies to the west, the living room is south, a stairway leads us to the second-level rooms, and a door to the garage is east. On the northern wall is the front door to the outdoors.'
                # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
                world[0]['exits'] = {'n': 9, 's': 4, 'w': 1, 'e': 5, 'u':6}
            else:
                print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')
        # using shirt
        if event_id in [2]:
            print(events[event_id]['first_time_text'])
            #events[event_id]['done'] = True  always do the first time text then add to inventory if not already there
            for thing in things:
                if thing['name'].lower() == 'shirt':
                    if thing['on_person']:
                        return
                    thing['on_person'] = True
                    inventory_quantity = inventory_quantity + 1
        # assemble ring from 2 parts
        if event_id in [3]:
            necessary_parts = 0
            for thing in things:
                if thing['name'] == 'hex nut' and ( thing['location'] == current_room or thing['on_person'] == True ):
                    necessary_parts += 1
                if thing['name'] == 'shirt' and thing['on_person'] == True:
                    necessary_parts += 1
            if necessary_parts == 2:
                things.append({'name': 'ring of power', 'prefix': 'the',
                               'description': 'This silver ring glows and emits a faint hum.',
                               'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': True})
                inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
                delete_thing('hex nut')
                delete_thing('shirt')
                # new room
                world[12]['visible'] = True
                # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
                world[11][
                    'desc'] = 'The splintered planks of the pier jut into the murky lake. Rocks, lily pads, and cattails dot the surrounding waters. Dry land is to the southwest. You feel drawn into the water below.'
                print(events[event_id]['first_time_text'])
                # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
                world[11]['exits'] = {'sw': 10, 'd': 12}
            else:
                print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')
        # trident drops from mermaid upon death
        if event_id in [12]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM OR USE current_room VARIABLE
            things.append({'name': 'trident', 'prefix': 'a',
                           'description': 'This three-pronged spear looks like it could puncture anything. Unfortunately, your short turtle-arms can\'t use it as a weapon. Still, you might find a use for it.',
                           'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        # use shell button
        if event_id in [6]:
            if events[event_id]['done'] == True:
                print(events[event_id]['already_done_text'])
            else:
                print(events[event_id]['first_time_text'])
                events[event_id]['done'] = True
                do_multi_step_event(event_id)
        # use snail shell
        if event_id in [7]:
            if events[event_id]['done'] == True:
                print(events[event_id]['already_done_text'])
            else:
                print(events[event_id]['first_time_text'])
                events[event_id]['done'] = True
                do_multi_step_event(event_id)
        # use conch
        if event_id in [8]:
            if events[event_id]['done'] == True:
                print(events[event_id]['already_done_text'])
            else:
                print(events[event_id]['first_time_text'])
                events[event_id]['done'] = True
                do_multi_step_event(event_id)

        # use duckweed - healing
        if event_id in [9]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            player_hp = player_hp + random.randrange(0, 21) + 40
            if player_hp > 100:
                player_hp = 100
            player_wellness(player_hp, 100)
            delete_thing('duckweed')
        # use lake lettuce - healing
        if event_id in [10]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            player_hp = player_hp + random.randrange(0, 21) + 45
            if player_hp > 100:
                player_hp = 100
            player_wellness(player_hp, 100)
            delete_thing('lake lettuce')
        # use water grubs - healing
        if event_id in [11]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            player_hp = player_hp + random.randrange(0, 21) + 50
            if player_hp > 100:
                player_hp = 100
            player_wellness(player_hp, 100)
            delete_thing('water grubs')
        # pop balloon make pipe accessible
        if event_id in [4]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # new room becomes visible
            world[37]['visible'] = True
            # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
            world[22][
                'desc'] = 'Jagged rocks make up the walls of this tunnel that runs from the southwest to the northeast. Now that the bladder is removed, a circular opening leads east.'
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[22]['exits'] = {'e': 37, 'sw': 21, 'ne': 23}
            delete_thing('air bladder')
        # remove key from blob
        if event_id in [13]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'rusty key', 'prefix': 'the',
                           'description': 'It\'s a key. It\'s rusty. There has to be a use for it.',
                           'location': 999, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False})
            inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
            delete_thing('curious blob')
        # blob drops from algae upon death
        if event_id in [14]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM OR USE current_room VARIABLE
            things.append({'name': 'curious blob', 'prefix': 'a',
                           'description': 'Yuck. It looks like a huge booger. If it didn\'t seem important, you would get far away from the sickly glob.',
                           'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        # use fountain to cleanse blob and get key
        if event_id in [15]:
            # item_index = ['curious blob' in i['name'] for i in things].index(True)
            # check to see if curious blob has been created
            for thing in things:
                if thing['name'].lower() == 'curious blob':
                    if thing['location'] == current_room or thing['on_person'] == True:
                        print(events[event_id]['first_time_text'])
                        events[event_id]['done'] = True
                        # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
                        things.append({'name': 'rusty key', 'prefix': 'the',
                                       'description': 'It\'s a key. It\'s rusty. There has to be a use for it.',
                                       'location': 999, 'on_person': True, 'moveable': True, 'is_weapon': False,
                                       'no_drop': False})
                        inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
                        delete_thing('curious blob')
                        return
            print('You hold your claws under the cleansing stream. Feels nice.')

        # unlock lobster trap to unleash crayfish
        if event_id in [16]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'busted trap', 'prefix': 'a',
                           'description': 'The lobster trap is a heap of twisted wire and splintered wood planks. It is still connected to the rope from above.',
                           'location': 40, 'on_person': False, 'moveable': False, 'is_weapon': False, 'base_damage': 0,
                           'damage': 0, 'hit_bonus': 0, 'no_drop': False})
            delete_thing('lobster trap')
            creatures.append({'id': 2, 'name': 'Crayfish',
                              'description': 'This hulking creature darts about, snapping its pincers wildly.',
                              'room': 40, 'max_hp': 120, 'current_hp': 120, 'is_dead': False, 'is_hostile': True,
                              'status_neutral': 'It swims in circles around you.', 'status_hostile': 'It readies to attack.',
                              'damage': 15, 'hit_bonus': 10, 'attack_chance': 70, 'is_fatigued': False, 'death_event': 17, 'was_seen': False,
                              'dead_description': 'The thick-shelled crustacean floats listlessly on the lake floor.' })
            show_creatures(current_room)
        # broken pincers drop from crayfish upon death
        if event_id in [17]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM OR USE current_room VARIABLE
            things.append({'name': 'broken pincers', 'prefix': 'the',
                           'description': 'It looks like you could slide your claws into these dark weapons of the crayfish.',
                           'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False,
                           'base_damage': 0, 'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        # use broken pincers to create on-player pincers and release sea serpent
        if event_id in [19]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'pincers', 'prefix': 'your',
                           'description': 'These claw-like appendages are gleaming black. The inner grip is dotted with a cutting edge of gnarly teeth.',
                           'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': True,
                           'base_damage': 20,
                           'damage': 50, 'hit_bonus': 35, 'no_drop': True})
            inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
            delete_thing('broken pincers')
            delete_thing('claws')
            print('A familiar surge of mystical energy runs through you. Your shell is harder, your limbs are more powerful, and your health is restored. You feel invincible! And my, what deadly pincers you have.')
            print('You are now a MEGA-TURTLE. When in combat, use your PINCERS to attack and your SHELL for protection.')
            player_hp = 100
            # add sea serpent to slimy core
            creatures.append({'id': 2, 'name': 'Sea serpent',
                              'description': 'This terrifying snake has deep blue scales and penetrating yellow eyes. A flame-red tongue flickers impatiently. As its tremendous length coils over itself, you are convinced it belongs in a much larger body of water.',
                              'room': 35, 'max_hp': 300, 'current_hp': 300, 'is_dead': False, 'is_hostile': False,
                              'status_neutral': 'It flashes its lethal fangs in a cruel smirk.', 'status_hostile': 'It is poised to strike!',
                              'damage': 5, 'hit_bonus': 10, 'attack_chance': 65, 'is_fatigued': False, 'death_event': 20, 'was_seen': False,
                              'dead_description': 'The grisly body of the snake winds around the lake floor. What a mess.' })
            # print message based on player location
            if current_room == 35:
                print('\nFrom the hole in the eastern wall, a massive serpent slithers into the cavern.')
                show_creatures(current_room)
            else:
                print('\nYou hear an unsettling sound in the distance. Something slithers in the deep.')
        # restore jewel drops from sea serpent upon death
        if event_id in [20]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM OR USE current_room VARIABLE
            things.append({'name': 'gem of restoration', 'prefix': 'the',
                           'description': 'An irrevocable power emanates from the deep blue depths of this jewel. One you use it, there\'s no turning back.',
                           'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False,
                           'base_damage': 0, 'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        # use restore gem to end game
        if event_id in [21]:
            print(events[event_id]['first_time_text'])
            room = 2
            events[event_id]['done'] = True



def do_special(current_room):
    global things
    global player_hp
    global special_done
    global inventory_quantity
    global locale_visited

    # print('game_choice: ', game_choice)
    if game_choice == '3':
        # bad air damage in any room outside of detention level if breathing mask not in inventory
        if current_room >= 5:
            for thing in things:
                # print('thing name: ', thing['name'].lower())
                if thing['name'].lower() == 'breathing mask':
                    if not thing['on_person']:
                        print('The air is too thin to breathe. You feel your lungs shriveling.')
                        bad_air_damage = 30
                        player_hp -= bad_air_damage
                        player_wellness(player_hp, 100)
        if current_room == 43:
            if not creatures[3]['is_dead']:
                if creatures[3]['is_hostile'] == False and special_done[0]['done'] == False:
                    print('The ship\'s captain is standing in the middle of the room. They speak to you in a haughty tone:'
                          '\n\t"So you survived. I had to bring the virus on board to see if it was effective. It was, even against a crew that fought back.'
                          '\n\tWe will learn much from our discovery. No one needs to know about our role in this."\n')
                    special_done[0]['done'] = True
                if creatures[3]['is_hostile'] == True and special_done[1]['done'] == False:
                    print('\nWith disdain, the captain utters:'
                        '\n\t"If you aren\'t willing to go along, you must be silenced. What\'s one more among the dead? \n\tYou will never make it off my ship!"\n')
                    special_done[1]['done'] = True
    elif game_choice == '4':
        if current_room == 12 and special_done[0]['done'] == False:
            print('When you enter the water, a surge of mystical energy runs through you. Your whole being quickly transforms into something smaller with a hard-back SHELL and fierce CLAWS.')
            print('You are a TURTLE. When in combat, use your claws to attack and your shell for protection.')
            for thing in things:
                if thing['name'] == 'claws':
                    thing['on_person'] = True
                    inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
                if thing['name'] == 'shell':
                    thing['on_person'] = True
                    inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
            special_done[0]['done'] = True
        if (current_room in [30, 31, 32, 33]) and locale_visited == False:
            special_chance = random.randrange(1, 101)
            if special_chance >= 67: # harm
                special_type = random.randrange(1, 7)
                if special_type == 1:
                    print('A hawk swoops down from the sky, delivering a mean scratch with its talons! It flies off before you can react.')
                elif special_type == 2:
                    print('A black crow flies over from a nearby tree. It pecks at you with its dark beak before darting away.')
                elif special_type == 3:
                    print('A blue heron sneaks up behind you and tries gnawing on your leg! It gets tiny chunk of your flesh and stalks off.')
                elif special_type == 4:
                    print('From the shore, an athletic racoon lunges at you before falling into the water.')
                elif special_type == 5:
                    print('A red fox pounces onto your shell, nipping at your head! After some chaotic gnawing, it scampers away.')
                else:
                    print('Two kids on the shore throw rocks at you, trying to knock you back into the lake. One of the rocks gives you a nasty cut!')
                special_damage = random.randrange(2, 9) # 2-8 damage
                player_hp = player_hp - special_damage
                if player_hp <= 0:
                    player_hp = 1
                player_wellness(player_hp, 100)

            elif special_chance >= 34: # benefit
                special_type = random.randrange(1, 4)
                if special_type == 1:
                    print('The clouds part, and a warm sunbeam lands on your shell. The heat gives you a delightful boost.')
                elif special_type == 2:
                    print('A plump fly buzzes into your open mouth. You chew and swallow the protein-filled treat. Yum!')
                else:
                    print('You spot a sneaky teenager on the shore, holding their phone towards you. They snap a pic and post it. You\'re famous! Well, Internet famous.')
                special_heal = random.randrange(2, 11) # 2-10 heal
                player_hp = player_hp + special_heal
                if player_hp >= 100:
                    player_hp = 100
                player_wellness(player_hp, 100)
            else: # nothing happens
                special_type = random.randrange(1, 4)
                if special_type == 1:
                    print('You enjoy a moment of peace.')
                elif special_type == 2:
                    print('Looking around at the still water gives you a moment to catch your breath.')
                else:
                    print('A gentle breeze plays across your round body. Feels nice.')
                player_wellness(player_hp, 100)
        if room_has_mobs == False and current_room > 12 and current_room < 30: # inside most of the lake and no mobs present
            special_chance = random.randrange(1, 101)
            if special_chance >= 79:
                special_type = random.randrange(1, 6)
                if special_type == 1:
                    print('A tiny, moss-covered twig floats by.')
                elif special_type == 2:
                    print('You see a rare freshwater shark zoom past. Yikes!')
                elif special_type == 3:
                    print('You notice a blue-green Gloeo bloom lazily wafting along.')
                elif special_type == 4:
                    print('In the corner you see a battered, orange leaf suspended in the water.')
                else:
                    print('A small school of minnows swarms nearby and then darts away.')



# checks if correct launch code is entered
def code_checker( ):
    global launch_code
    global room

    entered_code = input('Enter launch code: ')
    if room == 22 and entered_code.lower() == launch_code.lower():
        print('The console beeps happily. The screen reads: "LAUNCH SEQUENCE INITIATED"')
        room = 99
    else:
        print('The screen replies: INVALID LAUNCH CODE')


# function to check if certain creature is in same room as player
def creature_in_same_room( current_room, id):
    if creatures[id]['is_dead'] == False and creatures[id]['room'] == current_room:
        return True
    else:
        return False


def delete_thing(thing_name):
    global inventory_quantity
    for thing in things:
        if thing['name'] == thing_name:
            if thing['on_person']:
                inventory_quantity = inventory_quantity - 1
            things.remove(thing)


def show_exits(current_room):
    print('Visible exits:')
    for direction, destination in world[current_room]['exits'].items():
        if world[destination]['visible']:
            print(full_direction(direction) + world[destination]['name'])

def repeat_move():
    global target
    global choice
    global move
    global last_move

    repeat_response = input('Enter \'Y\' or \'Yes\' to repeat "' + last_move.lower() + '": ')
    if repeat_response.lower() == 'y' or repeat_response.lower == 'yes':
        choice = last_move.lower()
        target = extract_target(last_move)
        return choice.lower()
    else:
        return ""

def get_move():
    global target
    global choice
    global move
    global last_move

    print('What do you want to do?')
    choice = input()
    target = extract_target(choice)
    if choice.lower() == 'r' or choice.lower() == 'repeat':
        choice = repeat_move()
        return choice.lower()
    while not (choice.lower() in allowed_moves or choice.lower() in allowed_actions):
        print('"' + choice + '" is not recognized. Please try again.')
        print('What do you want to do?')
        choice = input()
        target = extract_target(choice)
    return choice.lower()


def extract_target(command):
    global choice
    space_index = command.find(' ')
    if space_index == -1:
        return ''
    else:
        choice = command[0:space_index]
        return command[(space_index + 1):]


def valid_move(from_key, direction):
    if direction in world[from_key]['exits'].keys():
        return True
    else:
        return False


def short_move(direction):
    if len(direction) == 9:
        return direction[0] + direction[5]
    elif direction == 'up':
        return direction[0]
    elif len(direction) == 2:
        return direction[0] + direction[1]
    elif len(direction) > 1:
        return direction[0]
    else:
        return direction


def full_direction(short_dir):
    if short_dir == 'n':
        return 'North - '
    if short_dir == 's':
        return 'South - '
    if short_dir == 'e':
        return 'East  - '
    if short_dir == 'w':
        return 'West  - '
    if short_dir == 'u':
        return 'Up    - '
    if short_dir == 'd':
        return 'Down  - '
    if short_dir == 'ne':
        return 'Northeast - '
    if short_dir == 'nw':
        return 'Northwest - '
    if short_dir == 'se':
        return 'Southeast - '
    if short_dir == 'sw':
        return 'Southwest - '


def show_help():
    global move
    global last_move

    print('COMMANDS'.center(72, '='))
    print('Here\'s a list of commands. They ARE NOT case sensitive.')
    print('To move around, you can type:')
    print('\t\'N\' or \'North\' to go north')
    print('\t\'NE\' or \'Northeast\' to go northeast')
    print('\t\'NW\' or \'Northwest\' to go northwest')
    print('\t\'S\' or \'South\' to go south')
    print('\t\'SE\' or \'Southeast\' to go southeast')
    print('\t\'SW\' or \'Southwest\' to go southwest')
    print('\t\'E\' or \'East\' to go east')
    print('\t\'W\' or \'West\' to go west')
    print('\t\'U\' or \'Up\' to go up')
    print('\t\'D\' or \'Down\' to go down')
    print('')
    print('To do things with items, you can type:')
    print('\t\'Use\' to use an item')
    print('\t\'X\' or \'Examine\' to inspect an item')
    print('\t\'Take\' to pick up an item and put it in your inventory')
    print('\t\'Drop\' to get rid of an item')
    print('You can type the action (use, examine, take, or drop) and the item name, or just the action.')
    print('For example: If you want to use the apple, you can type \'use apple\' or \'use.\'')
    print('If you just type \'use,\' you will be asked what item you want to use.')
    print('')
    print('A few notes about creatures and combat:')
    print('Creatures can be friendly or hostile (mean).')
    print('If you use a weapon near a friendly creature, you will be asked if you want to attack it.')
    print('Attacking a friendly creature will make it hostile, obviously.')
    print('Using a weapon near a hostile creature will always attack it.')
    print('Hostile creatures will attack and follow you until stopped.')
    print('')
    print('Other commands include:')
    print('\t\'L\' or \'Look\' to look around')
    print('\t\'I\' or \'Inv\' or \'Inventory\' to see what you are carrying')
    print('\t\'H\' or \'Health\' to check how you\'re feeling')
    print('\t\'R\' or \'Repeat\' to repeat the last valid command (without re-typing the whole thing!)')
    print('\t\'V\' or \'Verbose\' to turn OFF and ON the automatic display of visible exits')
    print('\t\'Save\' to save your progress')
    print('\t\'Load\' to load your progress from a game you saved earlier')
    print('\t\'?\' or \'Help\' to see this list of commands')
    print('\t\'Quit\' to quit the game')
    print('COMMANDS'.center(72, '='))
    last_move = move


def toggle_verbose():
    global verbose_mode

    if verbose_mode == True:
        verbose_mode = False
        print('Verbose mode is turned OFF. Use the \'Look\' command to see a list of visible exits.')
        print('If you want to switch back to Verbose mode, type \'V\' or \'Verbose\'.')
    else:
        verbose_mode = True
        print('Verbose mode is turned ON. Visible exits will automatically display when entering a location.')
        print('If you want to turn OFF Verbose mode, type \'V\' or \'Verbose\'.')


def save_game():
    # game will allow user to save game progress whether saved game exists or not
    if check_for_saved_games('save', game_choice):
        print('Are you sure you want to save your current progress and overwrite this earlier saved game?')
    else:
        print('Are you sure you want to save your progress?')
    save_confirm = input()
    if save_confirm.lower() == 'y' or save_confirm.lower() == 'yes':
        print('We will keep track of which game # you are playing and the time you saved.')
        saved_game_note = input('Enter a note about your progress: ')
        unformatted_save_time = datetime.datetime.now()
        save_time = unformatted_save_time.strftime("%B %d, %Y at %H:%M:%S %p")
        print(try_save_game(game_choice, save_time, saved_game_note))
    else:
        print('Okay, back to it.')

def load_saved_game( ):
    if check_for_saved_games('load', game_choice):
        print('Are you sure you want to overwrite your current progress with this saved game?')
        load_confirm = input()
        if load_confirm.lower() == 'y' or load_confirm.lower() == 'yes':
            print(try_load_saved_game( game_choice))
            locale(room)
        else:
            print('Okay, back to it.')

def check_for_saved_games(action, game):
    encoded_saved_game_file = 'saved_game' + game + '.sav'

    try:
        with open(encoded_saved_game_file, 'r') as f:
            base64_data = f.read()
        decoded_saved_data = base64.b64decode(base64_data)
        saved_data = json.loads(decoded_saved_data)

    except FileNotFoundError:
        if action == 'save': # attempting to save game, file not found, ok to save
            return False
        else: # attempting to load game, file not found, give news
            print('Sorry. Saved game progress not found.')
            return False
    else:
        if action == 'save': # attempting to save game, file found, give warning
            print('WARNING: This will overwrite your saved game progress.')
            print('We found this saved game progress: Game # ' + str(saved_data['saved_game_choice']) + ' on ' + str(saved_data['saved_game_time']) + ' with note: ' + str(saved_data['saved_game_note']))
            return True
        else: # attempting to load game, file found, ok to load
            print('WARNING: Loading a game will overwrite your current progress.')
            print('We found this saved game progress: Game # ' + str(saved_data['saved_game_choice']) + ' on ' + str(saved_data['saved_game_time']) + ' with note: ' + str(saved_data['saved_game_note']))
            return True


def try_save_game( game, time, note):
    #global saved_data
    global things
    global world
    global events
    global room
    global last_move
    global player_hp
    global creatures
    global inventory_quantity
    global special_done
    global safe_rooms
    global launch_code
    global exit_room
    global intro_text
    global outro_text
    global room_has_items
    global room_has_mobs
    global locale_visited
    global special_rooms
    global verbose_mode

    saved_data = { 'saved_game_choice': game,
                   'saved_game_time': time,
                   'saved_game_note': note,
                   'saved_things': things,
                   'saved_world': world,
                   'saved_events': events,
                   'saved_room': room,
                   'saved_last_move': last_move,
                   'saved_player_hp': player_hp,
                   'saved_creatures': creatures,
                   'saved_inventory_quantity': inventory_quantity,
                   'saved_special_done': special_done,
                   'saved_safe_rooms': safe_rooms,
                   'saved_launch_code': launch_code,
                   'saved_exit_room': exit_room,
                   'saved_intro_text': intro_text,
                   'saved_outro_text': outro_text,
                   'saved_room_has_items': room_has_items,
                   'saved_room_has_mobs': room_has_mobs,
                   'saved_locale_visited': locale_visited,
                   'saved_special_rooms': special_rooms,
                   'saved_verbose_mode': verbose_mode
                   }
    encoded_saved_game_file = 'saved_game' + game + '.sav'

    json_saved_data = json.dumps(saved_data)
    encoded_saved_data = base64.b64encode(json_saved_data.encode('utf-8'))

    try:
        with open(encoded_saved_game_file, "wb") as file:
            file.write(encoded_saved_data)
    except FileNotFoundError:
        return 'Sorry. We could not save your game. Contact Tech Support.\n'
    else:
        return 'Saved: Game # ' + str(game) + ' on ' + str(time) + ' with note: ' + str(note)


def try_load_saved_game( game ):
    #global saved_data
    global things
    global world
    global events
    global room
    global last_move
    global player_hp
    global creatures
    global inventory_quantity
    global special_done
    global safe_rooms
    global launch_code
    global exit_room
    global intro_text
    global outro_text
    global room_has_items
    global room_has_mobs
    global locale_visited
    global special_rooms
    global verbose_mode

    encoded_saved_game_file = 'saved_game' + game + '.sav'

    try:
        with open(encoded_saved_game_file, 'r') as f:
            base64_data = f.read()
        decoded_saved_data = base64.b64decode(base64_data)
        saved_data = json.loads(decoded_saved_data)
    except FileNotFoundError:
        return 'Sorry. We could not load your game. Contact Tech Support.\n'

    things = saved_data['saved_things']
    world = saved_data['saved_world']
    events = saved_data['saved_events']
    room = saved_data['saved_room']
    last_move = saved_data['saved_last_move']
    player_hp = saved_data['saved_player_hp']
    creatures = saved_data['saved_creatures']
    inventory_quantity = saved_data['saved_inventory_quantity']
    special_done = saved_data['saved_special_done']
    safe_rooms = saved_data['saved_safe_rooms']
    launch_code = saved_data['saved_launch_code']
    exit_room = saved_data['saved_exit_room']
    intro_text = saved_data['saved_intro_text']
    outro_text = saved_data['saved_outro_text']
    room_has_items = saved_data['saved_room_has_items']
    room_has_mobs = saved_data['saved_room_has_mobs']
    locale_visited = saved_data['saved_locale_visited']
    special_rooms = saved_data['saved_special_rooms']
    verbose_mode = saved_data['saved_verbose_mode']
    return('Game loaded!\n')


def show_short_help():
    print('Enter \'?\' or \'Help\' to see a list of commands.')


def show_intro():
    show_short_help()
    print('')
    print(intro_text)
    #input('Press ENTER to continue...')
    #show_help()
    #print('')
    #print('Good luck and have fun!')
    #print('')


def clear_game_vars():
    global world
    global things
    global events
    global creatures
    world = []
    things = []
    events = []
    creatures = []


def load_game(choice):
    global world
    global things
    global events
    global creatures
    global player_hp
    global starting_room
    global exit_room
    global intro_text
    global outro_text
    global special_rooms
    global special_done
    global launch_code
    global safe_rooms
    clear_game_vars()

    if choice == '1':
        world.insert(0, {'visible': True, 'name': 'House', 'prefix': 'in the', 'name2': '',
                         'desc': 'This modest dwelling has one room on the ground floor. You can see the front yard to the east and the garage through a door to the south. One set of stairs leads up to the studio, and another goes down to the basement.',
                         'exits': {'e': 1, 's': 2, 'u': 8, 'd': 6}})
        world.insert(1, {'visible': True, 'name': 'Yard', 'prefix': 'in the', 'name2': '',
                         'desc': 'The grass in the front yard is browning, and the flowers look sad. You can go west to back into the house, or go south around the house to the garage. Outside of the yard to the east is a street.',
                         'exits': {'w': 0, 's': 2, 'e': 3}})
        world.insert(2, {'visible': True, 'name': 'Garage', 'prefix': 'in the', 'name2': '',
                         'desc': 'There is a musty smell, and oil stains cover the concrete floor. You can get to the house through the door to the north. The door to the yard is somehow stuck, but the main garage door to the east opens to the street.',
                         'exits': {'n': 0, 'e': 3}})
        world.insert(3, {'visible': True, 'name': 'Street', 'prefix': 'on the', 'name2': '',
                         'desc': 'You don\'t see any cars on this strikingly ordinary street. The house is nearby. To the north is the gate to the front yard, and the garage door is open to the west. You see a dusty junkyard to the east. Following the road south will bring you to a park.',
                         'exits': {'n': 1, 'w': 2, 'e': 9, 's': 4}})
        world.insert(4, {'visible': True, 'name': 'Park', 'prefix': 'at the', 'name2': '',
                         'desc': 'The wide, grassy clearing at the end of the road is accented by a few tall trees. Part of the grass is bare along the southern edge, and it contains a strange etching of a house and a winged creature. The street is at the north end of the park, a trail leads through the trees to the west, and a small meadow is to the east.',
                         'exits': {'n': 3, 'e': 10, 'w': 11}})
        world.insert(5, {'visible': False, 'name': 'Glowy portal', 'prefix': 'through the', 'name2': '', 'desc': 'End description',
                         'exits': {}})
        world.insert(6, {'visible': True, 'name': 'Basement', 'prefix': 'in the', 'name2': '',
                         'desc': 'It is really dark down here. And damp. Stairs lead back up into the house.',
                         'exits': {'u': 0}})
        world.insert(7, {'visible': False, 'name': 'Tree', 'prefix': 'up a', 'name2': '',
                         'desc': 'You climb to the upper branches of the newly sprouted tree.', 'exits': {'d': 4}})
        world.insert(8, {'visible': True, 'name': 'Studio', 'prefix': 'in the', 'name2': '',
                         'desc': 'An old painting hangs on the wall of this small space. Another wall has a large print of abstract shapes inside a circle. If you squint, you think the shapes represent something flying out of a tall structure, or they could be a square lollipop barfing feathers. A stairway goes back down to the main room.',
                         'exits': {'d': 0}})
        world.insert(9, {'visible': True, 'name': 'Junkyard', 'prefix': 'in the', 'name2': '',
                         'desc': 'The air is thick in this run-down yard. Rusty scrap metal and mismatched tires are strewn about. The exit, back to the street, is on the west end of the junkyard.',
                         'exits': {'w': 3}})
        world.insert(10, {'visible': True, 'name': 'Meadow', 'prefix': 'in the', 'name2': '',
                          'desc': 'This grassy spot is pleasant and wide. A lonely stone well sits in the middle. The park is to the west.',
                          'exits': {'w': 4}})
        world.insert(11, {'visible': True, 'name': 'Forest path', 'prefix': 'on the', 'name2': '',
                          'desc': 'The dense woods are pierced by a well-worn trail. Looking west, the path appears to open into a dell. To the east, you see the park.',
                          'exits': {'e': 4, 'w': 12}})
        world.insert(12, {'visible': True, 'name': 'Dell', 'prefix': 'in the', 'name2': '',
                          'desc': 'This gentle valley is surrounded by leafy trees and bushes. A path is visible to the east, and to the north you see a sturdy iron gate that fills the only opening in the foliage.',
                          'exits': {'e': 11}})
        world.insert(13, {'visible': False, 'name': 'Winding passageway', 'prefix': 'in a', 'name2': '',
                          'desc': 'This jaunty tunnel is dimly lit by bioluminescent lichen. So pretty! The open iron gate is at the south end of the passage. As it bends to the northeast, it goes deeper and deeper into the earth.',
                          'exits': {'s': 12, 'ne': 14}})
        world.insert(14, {'visible': True, 'name': 'Subbasement', 'prefix': 'in the', 'name2': '',
                          'desc': 'This tiny, chilly room opens west to a winding passageway. There\'s a trick one-way trapdoor in the ceiling, which you can access using handholds cut into the wall.',
                          'exits': {'sw': 13, 'u': 6}})

        starting_room = 0
        exit_room = 5
        safe_rooms = []
        player_hp = 100
        launch_code = ''

        things.append({'name': 'note', 'prefix': 'a',
                       'description': 'Something is badly scrawled on this yellowing paper, but with effort, you can read it. \n\'If you don\'t like it here, exit through the portal.\nObviously, portals aren\'t naturally occurring.\nYou\'ll have to summon one.\nI think there\'s a clue in the studio.\'',
                       'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'pebble', 'prefix': 'a',
                       'description': 'This tiny rock has been smoothed by eons of natural erosion. How could something so small be so old?',
                       'location': 1, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'ball', 'prefix': 'a', 'description': 'It\'s a dark pink playground ball.', 'location': 4,
                        'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'Mona Lisa', 'prefix': 'the',
                       'description': 'This painting is a masterpiece of the Italian Renaissance. There is something to that smile.',
                       'location': 8, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'tricycle', 'prefix': 'a',
                       'description': 'The light blue aluminum tricycle appears to be in working order, though that plastic seat doesn\'t seem comfortable.',
                       'location': 3, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'tree kit', 'prefix': 'a',
                       'description': 'The tree kit box claims: \'Makes a real life tree in seconds! No digging required. For best results, use in an open area.\'',
                       'location': 2, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'egg', 'prefix': 'an',
                       'description': 'The small, blue egg feels weighty, like there\'s something inside it.',
                       'location': 7, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'post', 'prefix': 'a',
                       'description': 'It\'s four feet tall, stuck in the ground, and has a little square table surface at the top.',
                       'location': 1, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'machine', 'prefix': 'a',
                       'description': 'You try to make sense of this large, well-maintained, metallic box. It is the size of a refrigerator but without any visible doors. It has two holes: a small slot near the top and a large square hole at the bottom.',
                       'location': 9, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'broken well', 'prefix': 'a',
                       'description': 'It looks like this old well isn\'t completely broken. The crank turns, adjusting the height of the rope, but nothing is attached to it. At the bottom of the well, something reflects light back up to you.',
                       'location': 10, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'bucket', 'prefix': 'a',
                       'description': 'This yellow bucket has a wide handle at the top, making it easy to hold.',
                       'location': 2, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'coin', 'prefix': 'a',
                       'description': 'This rusty coin has indecipherable symbols on one side and a rectangular shape on the other. It doesn\'t appear to be worth much.',
                       'location': 13, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'gate', 'prefix': 'a',
                       'description': 'This is a serious gate. The wrought-iron frame is elegant yet ominous. You see a bulky, brass lock mechanism that contains a happy keyhole.',
                       'location': 12, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False})

        # note: if room == 999 then event can be done in any room
        # possible issue: if item can be used in specific room & 999, does room# need to appear before 999 event? why?
        events.insert(0, {'id': 0, 'done': False, 'room': 8, 'item_name': 'Mona Lisa',
                          'first_time_text': 'Mona Lisa winks at you.',
                          'already_done_text': 'The portrait isn\'t doing anything else.'})
        events.insert(1, {'id': 1, 'done': False, 'room': 0, 'item_name': 'ball',
                          'first_time_text': 'Mom always said, \'Don\'t play ball in the house.\'',
                          'already_done_text': 'Seriously, \'Don\'t play ball in the house.\''})
        events.insert(2, {'id': 2, 'done': False, 'room': 4, 'item_name': 'tree kit',
                          'first_time_text': 'Though you can\'t find instructions, the tree kit is suprisingly easy to use. A huge tree shoots up from the earth.',
                          'already_done_text': 'The kit\'s reagents are all used up.'})
        events.insert(3, {'id': 3, 'done': False, 'room': 999, 'item_name': 'egg',
                          'first_time_text': 'You crack open the egg. A slimy robin emerges. It\'s shivering, so you put it in your pocket. The shell falls to your feet.',
                          'already_done_text': 'It\'s empty. There\'s little to do with the broken egg shell.'})
        events.insert(4, {'id': 4, 'done': False, 'room': 999, 'item_name': 'tricycle',
                          'first_time_text': 'You ride the tricycle around and around. Whee!',
                          'already_done_text': 'You ride the tricycle again. That fun never gets old.'})
        events.insert(5, {'id': 5, 'done': False, 'room': 6, 'item_name': 'flashlight',
                          'first_time_text': 'You shine the flashlight across the room. A tiny toy house is now visible on the floor.',
                          'already_done_text': 'There\'s nothing surprising when you use the flashlight.'})
        events.insert(6, {'id': 6, 'done': False, 'room': 1, 'item_name': 'toy house',
                          'first_time_text': 'You attach the toy house to the post. You\'ve made a birdhouse!',
                          'already_done_text': 'It looks perfect where it is. There\'s nothing more to do with it.'})
        events.insert(7, {'id': 7, 'done': False, 'room': 1, 'item_name': 'robin',
                          'first_time_text': 'You place the baby robin into the birdhouse. You hear a loud but pleasant cracking sound in the distance to the east and a little south.',
                          'already_done_text': 'The bird seems content already. Best leave it alone.'})
        events.insert(8, {'id': 8, 'done': False, 'room': 8, 'item_name': 'ball',
                          'first_time_text': 'Mom always said, \'Don\'t play ball in the house.\'',
                          'already_done_text': 'Seriously, \'Don\'t play ball in the house.\''})
        events.insert(9, {'id': 9, 'done': False, 'room': 6, 'item_name': 'ball',
                          'first_time_text': 'Mom always said, \'Don\'t play ball in the house.\'',
                          'already_done_text': 'Seriously, \'Don\'t play ball in the house.\''})
        events.insert(10, {'id': 10, 'done': False, 'room': 9, 'item_name': 'ball',
                           'first_time_text': 'You try to fit the ball into the bigger round hole of the machine, but it doesn\'t fit.',
                           'already_done_text': 'Try as you might, you still can\'t get the ball into the machine.'})
        events.insert(11, {'id': 11, 'done': False, 'room': 9, 'item_name': 'coin',
                           'first_time_text': 'You place the coin in the slot of the machine. It pings off metal within, causing gears to churn and grind. It goes silent for a few seconds, then a flashlight shoots out of the lower hole, narrowly missing your leg!',
                           'already_done_text': 'There\'s nothing more to do with it.'})
        events.insert(12, {'id': 12, 'done': False, 'room': 999, 'item_name': 'ball',
                           'first_time_text': 'You throw, catch, and bounce the ball. Fun stuff.',
                           'already_done_text': 'You throw, catch, and bounce the ball some more. Fun stuff.'})
        events.insert(13, {'id': 13, 'done': False, 'room': 999, 'item_name': 'note',
                           'first_time_text': 'Something is badly scrawled on this yellowing paper, but with effort, you can read it. \'If you don\'t like it here, exit through the portal. Obviously, portals aren\'t naturally occurring. You\'ll have to summon one. I think there\'s a clue in the studio.\'',
                           'already_done_text': 'Something is badly scrawled on this yellowing paper, but with effort, you can read it. \'If you don\'t like it here, exit through the portal. Obviously, portals aren\'t naturally occurring. You\'ll have to summon one. I think there\'s a clue in the studio.\''})
        events.insert(14, {'id': 14, 'done': False, 'room': 1, 'item_name': 'post',
                           'first_time_text': 'The post doesn\'t do anything by itself. Try using another item near it.',
                           'already_done_text': 'The post doesn\'t do anything by itself. Try using another item near it.'})
        events.insert(15, {'id': 15, 'done': False, 'room': 9, 'item_name': 'machine',
                           'first_time_text': 'You can\'t figure out how to get the machine to do anything. Try using another item near it.',
                           'already_done_text': 'You can\'t figure out how to get the machine to do anything. Try using another item near it.'})
        events.insert(16, {'id': 16, 'done': False, 'room': 10, 'item_name': 'broken well',
                           'first_time_text': 'Turning the crank lowers the line into the water and back up again. There\'s definitely something shiny at the bottom of the well, but it\'s too narrow to climb down.',
                           'already_done_text': 'Turning the crank lowers the line into the water and back up again. There\'s definitely something shiny at the bottom of the well, but it\'s too narrow to climb down.'})
        events.insert(17, {'id': 17, 'done': False, 'room': 10, 'item_name': 'bucket',
                           'first_time_text': 'You tie the rope around the bucket handle. You fixed the well!',
                           'already_done_text': 'Using the bucket now that it is attached doesn\'t do anything. Try something else?'})
        events.insert(18, {'id': 18, 'done': False, 'room': 10, 'item_name': 'well',
                           'first_time_text': 'By turning the crank, you lower the bucket into the well. It makes a small splash when it hits the bottom. You raise the bucket from the depths, and you see a moss covered key inside! You grab it, but it slips out of your hand onto the ground.',
                           'already_done_text': 'You lower and raise the bucket again, but you can\'t fish out anything else from the well.'})
        events.insert(19, {'id': 19, 'done': False, 'room': 10, 'item_name': 'pebble',
                           'first_time_text': 'You drop the pebble in the well. It caroms off the stone side then splashes at the bottom. Bloop.',
                           'already_done_text': 'There\'s nothing more to do with it.'})
        events.insert(20, {'id': 20, 'done': False, 'room': 12, 'item_name': 'key',
                           'first_time_text': 'The key glides into the lock! With some effort, you turn the key and pull open the gate. An eerie light is coming from the cave to the north.',
                           'already_done_text': 'Yep, the key still fits in the lock.'})

        intro_text = ('*** Welcome to OG Portal ***\n\n'
                      'Well, this is odd. You find yourself in an unfamiliar house.\nYou don\'t remember how you got here. You just know this isn\'t real.\nLook around and use things. '
                      'If the way forward is not clear, keep looking. And using.\n\nYou must escape and get back to reality!\n')
        outro_text = 'Congratulations! You escaped that odd world and are back in reality.'

    elif choice == '2':
        safe_rooms = []
        world.insert(0, {'visible': True, 'name': 'Start', 'prefix': 'at the', 'name2': '',
                         'desc': 'This bare room is an octagon. You see a door in the southeast wall.',
                         'exits': {'se': 1}})
        world.insert(1, {'visible': True, 'name': 'Exit', 'prefix': 'at the', 'name2': '',
                         'desc': 'Packed dirt covers the floor of this spacious arena. A door is in the northwest corner. On the south wall, the words "EXIT BELOW" are painted in what could be dried blood. Or maybe ketchup? Below it is a large pit covered by an old grate.',
                         'exits': {'nw': 0}})
        world.insert(2, {'visible': True, 'name': 'End', 'prefix': 'out the', 'name2': '', 'desc': 'End description', 'exits': {}})
        starting_room = 0
        exit_room = 2
        player_hp = 100
        launch_code = ''
        things.append({'name': 'hammer', 'prefix': 'a',
                       'description': 'It\'s a classic ball-peen hammer. Could do some real damage.', 'location': 0,
                       'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': 10, 'damage': 30, 'hit_bonus': 20, 'no_drop': False})
        things.append({'name': 'cog', 'prefix': 'a', 'description': 'This rusty machine cog is worn down from years of use.',
                        'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'elixir', 'prefix': 'an',
                       'description': 'A small glass bottle contains a bright green liquid. The label reads: "Drink for fast-acting relief."',
                       'location': 1, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'locked grate', 'prefix': 'a', 'description': 'An ancient lattice of metal strips blocks access to the pit below, and sweet freedom. There is a large lock with a dusty keyhole holding the grate in place.',
                        'location': 1, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False})
        events.insert(0, {'id': 0, 'done': False, 'room': 999, 'item_name': 'hammer',
                          'first_time_text': 'You swing the hammer.', 'already_done_text': 'You swing the hammer.'})
        events.insert(1, {'id': 1, 'done': False, 'room': 1, 'item_name': 'elixir',
                          'first_time_text': 'You open the bottle and gulp down the contents. It tastes like ecto-cooler. Regardless, you feel a surge of wellness in your body.',
                          'already_done_text': 'The small bottle is empty. What a shame.'})
        events.insert(3, {'id': 3, 'done': False, 'room': 999, 'item_name': 'magic key',
                          'first_time_text': 'As the monster crumbles into a heap, a metallic object clangs onto the floor.',
                          'already_done_text': 'Come on, think about it. You can figure this out.'})
        events.insert(2, {'id': 2, 'done': False, 'room': 1, 'item_name': 'magic key',
                          'first_time_text': 'You have to force the magic key into the keyhole, but when you turn it, the lock mechanism cracks apart. The grate slides open revealing a surprisingly inviting hole in the ground.',
                          'already_done_text': 'The pit is now accessible.'})

        creatures.append({'id': 0, 'name': 'Monster',
                          'description': 'The monster is about 7 feet tall, covered in yellow fur, and shows sharp teeth and claws.',
                          'room': 0, 'max_hp': 100, 'current_hp': 100, 'is_dead': False, 'is_hostile': False,
                          'status_neutral': 'It isn\'t interested in you.', 'status_hostile': 'It\'s very mad at you.',
                          'damage': 20, 'hit_bonus': 20, 'attack_chance': 75, 'is_fatigued': False, 'death_event': 3, 'was_seen': False,
                          'dead_description': 'The sharp teeth and claws of the monster aren\'t so scary now that it\'s dead.' })
        intro_text = '*** Welcome to Combat practice ***\n\nThis is just a small world to help you get used to combat.\nWhen you get tired of fighting, just drop into the pit.\nUnfortunately, the pit is covered by a locked grate. Who has the key?\m'
        outro_text = 'Welp, you survived. The real challenge lies ahead.'

    elif choice == '3':
        safe_rooms = []
        starting_room = 0
        exit_room = 99
        player_hp = 100
        launch_code = ''
        intro_text = ('*** Welcome to Space adventure ***\n\n'
                      'You are on the custodial crew of an intergalactic starship. Your ship\'s mission was to respond to a distress signal sent by another ship in a newly discovered planetary system.\n'
                      'While happily cleaning the lounge, you overheard that something got into the ship. The last thing you remember was getting hit hard on the head.\n\n'
                      'You awake in a locked cell...\n')
        outro_text = (
            'The escape pod instruments light up, and you feel the machinery around the pod shifting, preparing for launch. You buckle into a seat as you watch the launch bay doors open outside the pod.'
            '\n\nThe thrusters blast and the pod hurtles out of the ship. Deepspace Communications systems are active in the pod, and you start sending a distress call to be picked up.'
            '\n\nCongratulations! You did it!')

        world.insert(0, {'visible': True, 'name': 'Cell', 'prefix': 'in a', 'name2': '',
                         'desc': 'This cell has a single door to the north.',
                         'exits': {'n': 1}})
        world.insert(1, {'visible': True, 'name': 'Detention hallway', 'prefix': 'in the', 'name2': '',
                         'desc': 'This long hallway has an elevator bay to the west. The hallway continues to the east. There is an open cell to the south.',
                         'exits': {'w': 4, 'e': 2, 's': 0}})
        world.insert(2, {'visible': True, 'name': 'Back hallway', 'prefix': 'in the', 'name2': '',
                         'desc': 'This is the end of the detention hallway. Back west is the main hallway. A small doorway is on the north wall.',
                         'exits': {'w': 1, 'n': 3}})
        world.insert(3, {'visible': True, 'name': 'Storage nook', 'prefix': 'in a', 'name2': '',
                         'desc': 'The only exit from this room is south.',
                         'exits': {'s': 2}})
        world.insert(4, {'visible': True, 'name': 'Detention Level Elevator Bay', 'prefix': 'at the',
                         'name2': ' (to Main Deck)',
                         'desc': 'The elevator goes up to the Main Deck, but it requires a keycard to activate it. The detention hallway is to the east.',
                         'exits': {'e': 1}})
        world.insert(5, {'visible': False, 'name': 'Main Deck Elevator Bay 5', 'prefix': 'at',
                         'name2': ' (to Detention Level)',
                         'desc': 'The elevator goes down to the Detention Level. To the west is a security checkpoint.',
                         'exits': {'w': 6, 'd': 4}})
        world.insert(6, {'visible': True, 'name': 'Main Deck Security Desk', 'prefix': 'at a', 'name2': '',
                         'desc': 'This is the Main Deck Security Checkpoint. To the east is an elevator bay to the Detention Level. To the south is an elevator bay to the Engine Room. A walkway is visible to the west.',
                         'exits': {'e': 5, 's': 7, 'w': 8}})
        world.insert(7, {'visible': True, 'name': 'Main Deck Elevator Bay 4', 'prefix': 'at', 'name2': ' (to Engine Room)',
                         'desc': 'The elevator goes down to the Engine Room. To the north is a security checkpoint.',
                         'exits': {'n': 6, 'd': 14}})
        world.insert(8, {'visible': True, 'name': 'Walkway', 'prefix': 'in the', 'name2': '',
                         'desc': 'This walkway connects the Main Deck Security Desk to the East and a wide hallway to the West. North is an elevator bay to the Hangar.',
                         'exits': {'e': 6, 'n': 9, 'w': 10}})
        world.insert(9, {'visible': True, 'name': 'Main Deck Elevator Bay 3', 'prefix': 'at', 'name2': ' (to Hangar)',
                         'desc': 'The elevator goes down to the Hangar, but it is currently deactivated. To the south is a walkway.',
                         'exits': {'s': 8}})
        world.insert(10, {'visible': True, 'name': 'Wide hallway', 'prefix': 'in the', 'name2': '',
                          'desc': 'This wide hallway branches in several directions. To the east is a walkway. South is an elevator to the Armory. To the west, the hallway continues toward the front of the ship.',
                          'exits': {'e': 8, 's': 11, 'w': 12}})
        world.insert(11, {'visible': True, 'name': 'Main Deck Elevator Bay 2', 'prefix': 'at', 'name2': ' (to Armory)',
                          'desc': 'The elevator goes down to the Armory. The control panel requires a retina scan to activate. To the north is a wide, branching hallway.',
                          'exits': {'n': 10}})
        world.insert(12, {'visible': True, 'name': 'Funneling hallway', 'prefix': 'in a', 'name2': '',
                          'desc': 'The hallway narrows as it leads from east to west. At the east end is a wide, branching hallway. To the west is an elevator to the Crew Quarters. '
                                  'Hardly visible in the southwest corner of the room is a dim passage to the Custodial Supplies room.',
                          'exits': {'e': 10, 'w': 13, 'sw': 48}})
        world.insert(13, {'visible': True, 'name': 'Main Deck Elevator Bay 1', 'prefix': 'at', 'name2': ' (to Quarters)',
                          'desc': 'The elevator goes down to Crew Quarters, but it requires a keycard to activate it. To the east is a widening hallway.',
                          'exits': {'e': 12}})
        world.insert(14,
                     {'visible': True, 'name': 'Engine Room Elevator Bay', 'prefix': 'at the', 'name2': ' (to Main Deck)',
                      'desc': 'The elevator goes up to the Main Deck. To the east is the Engine Room.',
                      'exits': {'u': 7, 'e': 15}})
        world.insert(15, {'visible': True, 'name': 'Engine Room', 'prefix': 'in the', 'name2': '',
                          'desc': 'The loud, pusling motor fills up most of the room. To the north and south are fuel cell storage rooms. An equipment room is to the east. To the west is an elevator bay.',
                          'exits': {'n': 16, 'e': 17, 's': 18, 'w': 14}})
        world.insert(16, {'visible': True, 'name': 'North fuel cell storage', 'prefix': 'in the', 'name2': '',
                          'desc': 'This room is filled with unused fuel cells. The only exit is to the south.',
                          'exits': {'s': 15}})
        world.insert(17, {'visible': True, 'name': 'Engine Equipment Room', 'prefix': 'in the', 'name2': '',
                          'desc': 'Spare parts, tools, and complex monitoring consoles fill this room. To the west is the engine room.',
                          'exits': {'w': 15}})
        world.insert(18, {'visible': True, 'name': 'South fuel cell storage', 'prefix': 'in the', 'name2': '',
                          'desc': 'This room is filled with empty fuel cells. The only exit is to the north.',
                          'exits': {'n': 15}})
        world.insert(19, {'visible': True, 'name': 'Hangar Elevator Bay', 'prefix': 'at the', 'name2': ' (to Main Deck)',
                          'desc': 'The elevator goes up to the Main Deck. To the east is a wide entrance to the Hangar.',
                          'exits': {'u': 9, 'e': 20}})
        world.insert(20, {'visible': True, 'name': 'Hangar', 'prefix': 'in the', 'name2': '',
                          'desc': 'This large room contains supply crates and a small, disassembled starship. Escape pods are in the southeast and southwest corners of the room. To the west is the elevator bay.',
                          'exits': {'w': 19, 'se': 21, 'sw': 22}})
        world.insert(21, {'visible': True, 'name': 'Escape pod B14', 'prefix': 'in', 'name2': '',
                          'desc': 'This small pod is surprisingly comfortable. The exit to the Hangar is to the northwest.',
                          'exits': {'nw': 20}})
        world.insert(22, {'visible': True, 'name': 'Escape pod L07', 'prefix': 'in', 'name2': '',
                          'desc': 'This small pod is cozy. The exit to the Hangar is to the northeast.',
                          'exits': {'ne': 20}})
        world.insert(23, {'visible': True, 'name': 'Armory Elevator Bay', 'prefix': 'at the', 'name2': ' (to Main Deck)',
                          'desc': 'This elevator goes up to the Main Deck. To the south is a security checkpoint.',
                          'exits': {'u': 11, 's': 24}})
        world.insert(24, {'visible': True, 'name': 'Armory Security Desk', 'prefix': 'at the', 'name2': '',
                          'desc': 'This is the heavily-fortified Armory Security Desk. To the east is the Guard Auxilary. To the north is an elevator bay.',
                          'exits': {'n': 23, 'e': 25}})
        world.insert(25, {'visible': True, 'name': 'Guard Auxilary', 'prefix': 'in the', 'name2': '',
                          'desc': 'The scent of battle is inescapable. Two storage rooms are accessible: Weapons to the north and Supplies to the east. The security checkpoint is to the west.',
                          'exits': {'w': 24, 'n': 26, 'e': 27}})
        world.insert(26, {'visible': True, 'name': 'Weapons storage room', 'prefix': 'in the', 'name2': '',
                          'desc': 'Implements of destruction fill every corner of this room. Most of them are beyond understanding. The only exit is south.',
                          'exits': {'s': 25}})
        world.insert(27, {'visible': True, 'name': 'Armory supply room', 'prefix': 'in the', 'name2': '',
                          'desc': 'This room contains many strange devices on shelving units and in closets. The exit is to the west.',
                          'exits': {'w': 25}})
        world.insert(28, {'visible': False, 'name': 'Quarters Elevator Bay 3', 'prefix': 'at', 'name2': ' (to Main Deck)',
                          'desc': 'This elevator goes up to the Main Deck. To the north is the lounge.',
                          'exits': {'n': 29, 'u': 13}})
        world.insert(29, {'visible': True, 'name': 'Lounge', 'prefix': 'in the', 'name2': '',
                          'desc': 'The lounge is perfect for resting and recreation. Tables, comfy chairs, and several entertainment consoles are thoughtfully arranged. A wide observation deck is visible to the west. To the east is the dormitory. An elevator to the Main Deck is at the south end of the room.',
                          'exits': {'s': 28, 'w': 32, 'e': 30}})
        world.insert(30, {'visible': True, 'name': 'Dormitory', 'prefix': 'in the', 'name2': '',
                          'desc': 'Rows and rows of empty sleeping pods fill the room. To the east are what look like grooming facilities. The lounge is accessible to the west.',
                          'exits': {'w': 29, 'e': 31}})
        world.insert(31, {'visible': True, 'name': 'Crew Facilities', 'prefix': 'in the', 'name2': '',
                          'desc': 'Showers, steampods, and hygiene facilities are arranged to maximize privacy. There are a few odd items left in a ransacked supply closet. '
                                  'Rooms with toilets are to the north and south. The dormitory is to the west.',
                          'exits': {'n': 46, 's': 47, 'w': 30}})
        world.insert(32, {'visible': True, 'name': 'Observation Deck', 'prefix': 'in the', 'name2': '',
                          'desc': 'A floor-to-ceiling window fills the western wall, giving a breathtaking view of the stars before the ship. Tables and seating are positioned to provide a relaxing sight. '
                                  'Elevator bays are on each end of the large window. An elevator to the bridge is to the north, and an elevator to the mess hall & medical services is to the south. To the east is the lounge area.',
                          'exits': {'n': 33, 'e': 29, 's': 34}})
        world.insert(33, {'visible': True, 'name': 'Quarters Elevator Bay 1', 'prefix': 'at', 'name2': ' (to Bridge)',
                          'desc': 'This elevator goes up to the Bridge, but it requires a keycard to activate it. To the south is the observation deck.',
                          'exits': {'s': 32}})
        world.insert(34,
                     {'visible': True, 'name': 'Quarters Elevator Bay 2', 'prefix': 'at', 'name2': ' (to Mess & Medical)',
                      'desc': 'This elevator goes down to the Mess Hall and Medical Services, but it requires a keycard to activate it. The observation deck is to the north.',
                      'exits': {'n': 32}})
        world.insert(35, {'visible': True, 'name': 'Mess Hall and Medical Services Elevator Bay', 'prefix': 'at the',
                          'name2': ' (to Quarters)',
                          'desc': 'This elevator goes up to the Crew Quarters. To the east is the mess hall. South is a room called Medical Services A.',
                          'exits': {'e': 38, 's': 36, 'u': 34}})
        world.insert(36, {'visible': True, 'name': 'Medical Services A', 'prefix': 'in', 'name2': '',
                          'desc': 'There is a small waiting area and a desk. To the north is an elevator bay. East is a room labeled Medical Services B.',
                          'exits': {'n': 35, 'e': 37}})
        world.insert(37, {'visible': True, 'name': 'Medical Services B', 'prefix': 'in', 'name2': '',
                          'desc': 'Several cubbies with desks and chairs are situated in each corner. The east wall is filled with cabinets and drawers. The only exit is to the west.',
                          'exits': {'w': 36}})
        world.insert(38, {'visible': True, 'name': 'Mess Hall', 'prefix': 'in the', 'name2': '',
                          'desc': 'This large room has neat rows of tables and a service area. The kitchen entrance is next to the service area on the north wall. Large double-doors connect a storage closet to the east. An elevator bay is to the west.',
                          'exits': {'n': 39, 'e': 41, 'w': 35}})
        world.insert(39, {'visible': True, 'name': 'Kitchen', 'prefix': 'in the', 'name2': '',
                          'desc': 'All kinds of food preparation and preservation devices are visible. A service area and doorway to the mess hall is to the south. The east wall connects to a deep walk-in pantry.',
                          'exits': {'s': 38, 'e': 40}})
        world.insert(40, {'visible': True, 'name': 'Pantry', 'prefix': 'in the', 'name2': '',
                          'desc': 'Dry and packaged foodstuffs in boxes, bins, and bags line the shelves. A cold-storage unit is built into the north wall. To the west is the kitchen.',
                          'exits': {'w': 39}})
        world.insert(41, {'visible': True, 'name': 'Storage and cleaning closet', 'prefix': 'in the', 'name2': '',
                          'desc': 'This well-stocked closet holds dining implements, cleaning solutions, and scrubbing mechanisms. There\'s also a cabinet of tools. The mess hall is to the west.',
                          'exits': {'w': 38}})
        world.insert(42, {'visible': True, 'name': 'Bridge Elevator Bay', 'prefix': 'at the', 'name2': ' (to Quarters)',
                          'desc': 'This elevator goes down to the Crew Quarters. To the north is a security checkpoint.',
                          'exits': {'d': 33, 'n': 43}})
        world.insert(43, {'visible': True, 'name': 'Bridge Security Desk', 'prefix': 'at the', 'name2': '',
                          'desc': 'This is the bridge-level security desk. A door to the bridge is to the west, but it is shut. To the east is the Systems Control room. South is an elevator bay.',
                          'exits': {'e': 45, 's': 42}})
        world.insert(44, {'visible': False, 'name': 'Bridge', 'prefix': 'on the', 'name2': '',
                          'desc': 'Even though it is called a bridge, it is more like a glorified cockpit. Flight controls and communications consoles are positioned near the officer chairs. East is the security desk.',
                          'exits': {'e': 43}})
        world.insert(45, {'visible': True, 'name': 'Systems Control room', 'prefix': 'in the', 'name2': '',
                          'desc': 'Data from the ship\'s environment control, propulsion, and weapons systems are a few of things displayed on huge screens in this room. The only way out is west to the security desk.',
                          'exits': {'w': 43}})
        world.insert(46, {'visible': True, 'name': 'Toilet Bank 1', 'prefix': 'in', 'name2': '',
                          'desc': 'An impressive number of toilets and bidets are discretely concealed within ceiling-to-floor privacy screens. The Crew Facilities are accessible to the south.',
                          'exits': {'s': 31}})
        world.insert(47, {'visible': True, 'name': 'Toilet Bank 2', 'prefix': 'in', 'name2': '',
                          'desc': 'An impressive number of toilets and bidets are discretely concealed within ceiling-to-floor privacy screens. The Crew Facilities are accessible to the north.',
                          'exits': {'n': 31}})
        world.insert(48, {'visible': True, 'name': 'Custodial Supplies room', 'prefix': 'in the', 'name2': '',
                          'desc': 'This dingy space contains an array of maintenance tools and equipment. To the northeast is the Funneling hallway. On the west side of the room is a door marked Workroom. '
                                  'It is locked, but the door knob has an old-fashioned keyhole in it.',
                          'exits': {'ne': 12}})
        world.insert(49, {'visible': False, 'name': 'Workroom', 'prefix': 'in the', 'name2': '',
                          'desc': 'The familiar workroom has decent lighting and ample space to fix or build all kinds of things. '
                                  'The only exit is back east to the Custodial Supplies room.', 'exits': {'e': 48}})

        things.append({'name': 'food tray', 'prefix': 'a',
                       'description': 'The empty food tray has some heft to it. The metal edge looks mean.',
                       'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': 10,
                       'damage': 10, 'hit_bonus': 25, 'no_drop': False})
        things.append({'name': 'stimpack', 'prefix': 'a',
                       'description': 'A small vial of clear liquid has a tiny needle on one end and a red heart decal on the side.',
                       'location': 3, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'breathing mask', 'prefix': 'a',
                       'description': 'The compact device looks like it would fit nicely on your face if you pick it up or use it.',
                       'location': 3, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'digipad1', 'prefix': 'a',
                       'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                      '\n\tAfter we were attacked, I dragged you in here and set the door to lock from the inside.'
                                      '\n\tYou can get out but be careful: most of the crew is dead. Those that survived are, well, dangerous.'
                                      '\n\tUse whatever you can to survive. You gotta get off this ship. -B',
                       'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'digipad2', 'prefix': 'a',
                       'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                      '\n\tSome kind of virus swept through the ship. It killed most of the crew. Others were corrupted.'
                                      '\n\tThey do not need oxygen. They are diverting the ship\'s oxygen for some other purpose.'
                                      '\n\tI preserved the atmosphere settings on the Detention Level, but other places on the ship are probably bad. -B',
                       'location': 2, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'wrench', 'prefix': 'a',
                       'description': 'The heavy tool is rusted, but it could do some real damage.',
                       'location': 17, 'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': 15,
                       'damage': 15, 'hit_bonus': 30, 'no_drop': False})
        things.append({'name': 'fuel cell', 'prefix': 'a',
                       'description': 'This metallic cylinder emits a strange bluish glow from a slit on each end. A warning label reads: DANGER - Will burn through organic matter.',
                       'location': 16, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'corpse', 'prefix': 'a',
                       'description': 'The body of one of your crewmates lies on the floor, contorted in an unnatural pose. Every inch of their body is covered in a wet, dark gray-green substance. '
                                      'It is translucent and looks hard, almost stone-like.',
                       'location': 10, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'digipad5', 'prefix': 'a',
                       'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                      '\n\tThe virus doesn\'t act the same on everybody. It doesn\'t make sense.'
                                      '\n\tI saw Jackson from Combat Services collapse. When she did, a jade crystal coating formed over her skin.'
                                      '\n\tOthers went into zombie mode and started attacking. -A',
                       'location': 8, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'allen claw', 'prefix': 'an',
                       'description': 'This shiny, angular piece of metal appears to have been fashioned for a specific purpose.',
                       'location': 41, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'smooth bar', 'prefix': 'a',
                       'description': 'This rod is painted orange. It has fittings on both ends.',
                       'location': 31, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append(
            {'name': 'gummy grip', 'prefix': 'a', 'description': 'The short pipe has a cushioned yet tackified surface.',
             'location': 27, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'dented tricorder', 'prefix': 'a',
                       'description': 'This banged-up scanner must be good for something. It still beeps!',
                       'location': 32, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'lockbox', 'prefix': 'a',
                       'description': 'There are cryptic symbols on this oblong box. The lid is fastened tight, but a square keyhole looks promising.',
                       'location': 18, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'scalpel', 'prefix': 'a',
                       'description': 'The surgical blade is short but exceedingly sharp. It would be very effective at a targeted procedure, but it could also do some damage in a fight if it connected.',
                       'location': 37, 'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': 10,
                       'damage': 25,
                       'hit_bonus': 15, 'no_drop': False})
        things.append({'name': 'fallen soldier', 'prefix': 'a',
                       'description': 'This dead crewmate is bent backwards, leaning on the countertop. They have the insignia and fatigues of a tactical combat specialist. '
                                      'Unlike the other bodies you encountered, this one seems frozen in shock, face up with eyes and mouth wide open.',
                       'location': 39, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'large stimpack', 'prefix': 'a',
                       'description': 'This device has 3 compact barrels of clear liquid that funnel into a small needle. You are comforted by the cheerful red heart logo on the top, '
                                      'and the encouraging label that reads, "Massive vitality boost."',
                       'location': 36, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'digipad4', 'prefix': 'a',
                       'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                      '\n\tThey say you can see it in the eyes when they\'re infected. They get all hazy.'
                                      '\n\tIf that\'s true, then it\'s happening to me. I can\'t see my own reflection any more. -L',
                       'location': 38, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'hot sauce', 'prefix': 'a',
                       'description': 'This small bottle has a picture of a burning crescent-shaped pepper. "One drop\'ll do ya!"',
                       'location': 40, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append(
            {'name': 'mayonnaise', 'prefix': 'a', 'description': 'The large jar of eggy, white, goop is still half-full.',
             'location': 40, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'pear powder', 'prefix': 'a',
                       'description': 'A hand-written label on this see-through bag describes the sparkly, yellow granules inside the flavor pouch.',
                       'location': 40, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'digipad3', 'prefix': 'a',
                       'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                      '\n\tTraining today in Systems Control. Learned how to activate locked down systems.'
                                      '\n\tThey got some real Rube Goldberg protocols. The lever that works the controls is'
                                      '\n\tassembled from three parts in storage on the ship. How is that secure? -M',
                       'location': 29, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'phaser', 'prefix': 'a',
                       'description': 'The V-8 phaser pistol is a reliable mid- to close-range weapon.',
                       'location': 26, 'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': 20,
                       'damage': 25, 'hit_bonus': 40, 'no_drop': False})
        things.append({'name': 'wound salve', 'prefix': 'a',
                       'description': 'The label on the opaque brown jar reads, "Apply liberally to cuts, welts, and lacerations." Inside is a substance that looks like pink jelly.',
                       'location': 27, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'digipad8', 'prefix': 'a',
                       # update this text
                       'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                      '\n\tThose infected, zombies, whatever--they do not stop.'
                                      '\n\tMe and Barb held off 6 of them in the mess hall. Don\'t know why but food seemed to make them weak.'
                                      '\n\tOr maybe it just distracted them. Hope somebody sees this. -X',
                       'location': 24, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'code generator', 'prefix': 'a',
                       'description': 'Nestled between navigation consoles is a device labeled "Escape Pod Launch Code Generator." It looks like an old-timey vending machine. There\'s a shiny red button and a digital display.',
                       'location': 44, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'lockdown console', 'prefix': 'the',
                       'description': 'The lockdown console has a small screen that reads: \n\t"LOCKDOWN ENGAGED - Offline systems: Hangar elevator, Deepspace Communications, Escape pods"'
                                      '\nThere does not appear to be any way to interact with the console, but there is an empty lever socket just below the screen.',
                       'location': 45, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'launch controls', 'prefix': 'the',
                       'description': 'The launch controls look like a small terminal. There\'s a screen and a keyboard.',
                       'location': 21, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'launch console', 'prefix': 'the',
                       'description': 'The launch console looks like a small terminal. There\'s a screen and a keyboard.',
                       'location': 22, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'dead crewmate', 'prefix': 'a',
                       'description': 'You recognize Petty Officer Smith from your time at the academy. He was always in motion. Now his body lies still. It looks like he suffered several blaster wounds.',
                       'location': 32, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'dead engineer', 'prefix': 'a',
                       'description': 'It\'s hard to look at the engineer. Her arm is bending the wrong way, and her head was hit hard by something heavy. The damage is so extensive you can\'t even recognize her.',
                       'location': 15, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'retina scanner', 'prefix': 'a',
                       'description': 'The scanner is built-into a panel next to the elevator door. '
                                      'It sits at about eye-level and sheds a dull red glow.',
                       'location': 11, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'phaser booster', 'prefix': 'a',
                       'description': 'The booster is a shiny gray widget. In small print it reads, '
                                      '"Turns your V-8 into a V-9!"',
                       'location': 7, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'medium stimpack', 'prefix': 'a',
                       'description': 'The double vials have red hearts etched into their sides. There is only one needle, thankfully.',
                       'location': 30, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'clogged toilet', 'prefix': 'a',
                       'description': 'The flush mechanism is not responsive. The bowl is stuffed with what looks like a very wet dark blue cloth.',
                       'location': 47, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'astroplunger', 'prefix': 'an', 'description': 'Some technology can\'t be improved upon. '
                                                                              'Despite its fancy name, the wooden handle and dark rubber bulb are fashioned in the classic design.',
                       'location': 48, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append(
            {'name': 'workbench', 'prefix': 'the', 'description': 'With this state-of-the-art quantum-precision workbench, '
                                                                  'there\'s nothing you can\'t build! The urge to create is almost overwhelming.',
             'location': 49, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'digipad9', 'prefix': 'a',
                       'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                      '\n\tThey\'re hunting the custodial staff. I guess it\'s because we have access to so much of the ship.'
                                      '\n\tSome of the team is hiding their uniforms. I guess the dark blue color gives us away. -B',
                       'location': 6, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})
        things.append({'name': 'workbench manual', 'prefix': 'a',
                       'description': 'You scan the manual for relevant information.'
                                      '\n\t...Holding high-heat materials requires gloves reinforced with non-conductive fibers...'
                                      '\n\t...A workbench is only as effective as it is clean. Buy our patented Bleakwipes to keep your workspace factory-pure...'
                                      '\n\t...Most levers can be constructed with a bar, a grip for holding, and some kind of tip that will connect to...'
                                      '\n\t...Fuel cell containers are not worth modifying. StarClunk makes the best...',
                       'location': 12, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False})

        events.insert(0, {'id': 0, 'done': False, 'room': 999, 'item_name': 'food tray',
                          'first_time_text': 'You swing the food tray.', 'already_done_text': 'You swing the food tray.'})
        events.insert(1, {'id': 1, 'done': False, 'room': 999, 'item_name': 'stimpack',
                          'first_time_text': 'You jab the stimpack into your thigh. Heat rushes through your body, and you feel better.',
                          'already_done_text': 'The stimpack is used up.'})
        # note 999 event needs to come AFTER room-specific event
        events.insert(3, {'id': 3, 'done': False, 'room': 999, 'item_name': 'keycard',
                          'first_time_text': 'As the guard falls to the floor, a keycard falls from its pocket.',
                          'already_done_text': 'Judging by its markings, this seems like it would be useful at the Detention Elevator Bay.'})
        events.insert(2, {'id': 2, 'done': False, 'room': 4, 'item_name': 'keycard',
                          'first_time_text': 'The keycard fits nicely into the elevator console. You can now use the elevator!',
                          'already_done_text': 'This elevator is already accessible.'})
        events.insert(4, {'id': 4, 'done': False, 'room': 999, 'item_name': 'breathing mask',
                          'first_time_text': 'The mask fits snugly on your face.',
                          'already_done_text': 'The mask fits snugly on your face.'})
        events.insert(5, {'id': 5, 'done': False, 'room': 999, 'item_name': 'digipad1',
                          'first_time_text': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                             '\n\tAfter we were attacked, I dragged you in here and set the door to lock from the inside.\n\tYou can get out but be careful: most of the crew is dead. Those that survived are, well, dangerous.'
                                             '\n\tUse whatever you can to survive. You gotta get off this ship. -B',
                          'already_done_text': 'The digipad reads:'
                                               '\n\tAfter we were attacked, I dragged you in here and set the door to lock from the inside.\n\tYou can get out but be careful: most of the crew is dead. Those that survived are, well, dangerous.'
                                               '\n\tUse whatever you can to survive. You gotta get off this ship. -B'})
        events.insert(6, {'id': 6, 'done': False, 'room': 999, 'item_name': 'digipad2',
                          'first_time_text': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                             '\n\tSome kind of virus swept through the ship. It killed most of the crew. Others were corrupted.\n\tThey do not need oxygen. They are diverting the ship\'s oxygen for some other purpose.'
                                             '\n\tI locked the atmosphere settings on the Detention Level, but other places on the ship are probably bad. -B',
                          'already_done_text': 'The digipad reads:'
                                               '\n\tSome kind of virus swept through the ship. It killed most of the crew. Others were corrupted.\n\tThey do not need oxygen. They are diverting the ship\'s oxygen for some other purpose.'
                                               '\n\tI locked the atmosphere settings on the Detention Level, but other places on the ship are probably bad. -B'})
        events.insert(7, {'id': 7, 'done': False, 'room': 999, 'item_name': 'wrench',
                          'first_time_text': 'You heave the wrench in a fearsome arc.',
                          'already_done_text': 'You heave the wrench in a fearsome arc.'})
        events.insert(8, {'id': 8, 'done': False, 'room': 10, 'item_name': 'fuel cell',
                          'first_time_text': 'You pour the fuel cell onto the petrified corpse. The fuel melts through the green substance, producing a steamy sizzle. It also melts through the clothes and flesh. The stench is vile. '
                                             'After a few seconds of that horrific chemical reaction, all that remains in the puddle are a few metal fillings, a useless belt buckle, and a keycard.',
                          'already_done_text': 'The fuel cell is used up.'})
        events.insert(9, {'id': 9, 'done': False, 'room': 13, 'item_name': 'quarters keycard',
                          'first_time_text': 'The keycard fits nicely into the elevator console. You can now use the elevator!',
                          'already_done_text': 'This elevator is already accessible.'})
        events.insert(10, {'id': 10, 'done': False, 'room': 999, 'item_name': 'digipad5',
                           'first_time_text': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                              '\n\tThe virus doesn\'t act the same on everybody. It doesn\'t make sense.'
                                              '\n\tI saw Jackson from Combat Services collapse. Once she did, a jade-green crystallized coating formed over her skin.'
                                              '\n\tOthers went into zombie mode and started attacking. -A',
                           'already_done_text': 'The digipad reads:'
                                                '\n\tThe virus doesn\'t act the same on everybody. It doesn\'t make sense.'
                                                '\n\tI saw Jackson from Combat Services collapse. Once she did, a jade crystal coating formed over her skin.'
                                                '\n\tOthers went into zombie mode and started attacking. -A'})
        events.insert(12, {'id': 12, 'done': False, 'room': 999, 'item_name': 'mess keycard',
                           'first_time_text': 'As the zombie falls to the floor, a keycard falls from its pocket.',
                           'already_done_text': 'Judging by its markings, this seems like it would be useful at the Mess & Medical Elevator Bay.'})
        events.insert(11, {'id': 11, 'done': False, 'room': 34, 'item_name': 'mess keycard',
                           'first_time_text': 'The keycard fits nicely into the elevator console. You can now use the elevator!',
                           'already_done_text': 'This elevator is already accessible.'})
        events.insert(13, {'id': 13, 'done': False, 'room': 39, 'item_name': 'scalpel',
                           'first_time_text': 'After gathering resolve, you gently cut an eye out of the fallen soldier and slide it in your pocket. Yuck.',
                           'already_done_text': 'Haven\'t you butchered enough already?'})
        events.insert(14, {'id': 14, 'done': False, 'room': 999, 'item_name': 'scalpel',
                           'first_time_text': 'You slice with the scalpel.',
                           'already_done_text': 'You slice with the scalpel.'})
        events.insert(15, {'id': 15, 'done': False, 'room': 999, 'item_name': 'large stimpack',
                           'first_time_text': 'You jab the large stimpack into your thigh. Intense heat surges into your body, and you feel much, much better.',
                           'already_done_text': 'The large stimpack is used up.'})
        events.insert(16, {'id': 16, 'done': False, 'room': 999, 'item_name': 'digipad4',
                           'first_time_text': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                              '\n\tThey say you can see it in the eyes when they\'re infected. They get all hazy.'
                                              '\n\tIf that\'s true, then it\'s happening to me. I can\'t see my own reflection any more. -L',
                           'already_done_text': 'The digipad reads:'
                                                '\n\tThey say you can see it in the eyes when they\'re infected. They get all hazy.'
                                                '\n\tIf that\'s true, then it\'s happening to me. I can\'t see my own reflection any more. -L'})
        events.insert(17, {'id': 17, 'done': False, 'room': 11, 'item_name': 'soldier eye',
                           'first_time_text': 'You hold the clammy eyeball up to the retina scanner. After repositioning it, the control panel beeps twice '
                                              'and displays, "ARMORY ACCESS GRANTED." You can now use the elevator!',
                           'already_done_text': 'This elevator is already accessible.'})
        events.insert(18, {'id': 18, 'done': False, 'room': 999, 'item_name': 'soldier eye',
                           'first_time_text': 'You carefully pull the eye out of your pocket. There doesn\'t seem to be anything to do with it here. You gladly put it away.',
                           'already_done_text': 'You\'re reluctant to remove the eye from your pocket. It\'s slimy and feels like it is always looking at you.'})
        events.insert(19, {'id': 19, 'done': False, 'room': 999, 'item_name': 'digipad3',
                           'first_time_text': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                              '\n\tTraining today in Systems Control. Learned how to activate locked down systems.'
                                              '\n\tThey got some real Rube Goldberg protocols. The lever that works the controls is'
                                              '\n\tassembled from three parts in storage on the ship. How is that secure? -M',
                           'already_done_text': 'The digipad reads:'
                                                '\n\tTraining today in Systems Control. Learned how to activate locked down systems.'
                                                '\n\tThey got some real Rube Goldberg protocols. The lever that works the controls is'
                                                '\n\tassembled from three parts in storage on the ship. How is that secure? -M'})
        events.insert(20, {'id': 20, 'done': False, 'room': 33, 'item_name': 'bridge keycard',
                           'first_time_text': 'The keycard fits nicely into the elevator console. You can now use the elevator!',
                           'already_done_text': 'This elevator is already accessible.'})
        events.insert(21, {'id': 20, 'done': False, 'room': 999, 'item_name': 'bridge keycard',
                           'first_time_text': 'When the huge guard slumps to the floor, you notice it was holding a keycard in one of its clenched fists.',
                           'already_done_text': 'The keycard\'s markings indicate it could be used to access the Bridge elevator.'})
        events.insert(22, {'id': 22, 'done': False, 'room': 999, 'item_name': 'phaser',
                           'first_time_text': 'You fire the phaser.', 'already_done_text': 'You fire the phaser.'})
        events.insert(23, {'id': 23, 'done': False, 'room': 999, 'item_name': 'wound salve',
                           'first_time_text': 'You apply the salve to your most painful wounds. A cool tingling pulls the ache from your body. You feel better.',
                           'already_done_text': 'The wound salve is used up.'})
        events.insert(24, {'id': 24, 'done': False, 'room': 999, 'item_name': 'hot sauce',
                           'first_time_text': 'You hurl the bottle at the Hulking guard. It shatters and its contents splatter across the brute\'s chest and neck. It stumbles, looking diminished by the spicy assault.',
                           'already_done_text': 'The hot sauce is gone.'})
        events.insert(25, {'id': 25, 'done': False, 'room': 999, 'item_name': 'mayonnaise',
                           'first_time_text': 'You chuck the mayo jar at the Hulking guard. Bullseye! It breaks on its forehead, covering its face with cream-covered glass shards. That was a humiliating blow, even for a zombie.',
                           'already_done_text': 'The mayonnaise is gone.'})
        events.insert(26, {'id': 26, 'done': False, 'room': 999, 'item_name': 'pear powder',
                           'first_time_text': 'You dump the bag of pear powder on the Hulking guard. The yellow crystals stick to its flesh and clothes. The zombie recoils in self-disgust, weakened by the indignity.',
                           'already_done_text': 'The pear powder is gone.'})
        events.insert(27, {'id': 27, 'done': False, 'room': 999, 'item_name': 'digipad8',
                           'first_time_text': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                              '\n\tThose infected, zombies, whatever--they do not stop.'
                                              '\n\tMe and Barb iced 6 of them in the mess hall. Don\'t know why but food made them real mad.'
                                              '\n\tIt hurt them too. Hope somebody sees this. -X',
                           'already_done_text': 'The digipad reads:'
                                                '\n\tThose infected, zombies, whatever--they do not stop.'
                                                '\n\tMe and Barb held off 6 of them in the mess hall. Don\'t know why but food seemed to make them weak.'
                                                '\n\tOr maybe it just distracted them. Hope somebody sees this. -X'})
        events.insert(28, {'id': 28, 'done': False, 'room': 49, 'item_name': 'allen claw',
                           'first_time_text': 'When you lay your items on the workbench, you see what to do. The allen claw, smooth bar, and gummy grip fit together with a satisfying snap. '
                                              'You\'ve made the override lever!', 'already_done_text': 'Nothing happens.'})
        events.insert(29, {'id': 29, 'done': False, 'room': 49, 'item_name': 'smooth bar',
                           'first_time_text': 'When you lay your items on the workbench, you see what to do. The allen claw, smooth bar, and gummy grip fit together with a satisfying snap. '
                                              'You\'ve made the override lever!', 'already_done_text': 'Nothing happens.'})
        events.insert(30, {'id': 30, 'done': False, 'room': 49, 'item_name': 'gummy grip',
                           'first_time_text': 'When you lay your items on the workbench, you see what to do. The allen claw, smooth bar, and gummy grip fit together with a satisfying snap. '
                                              'You\'ve made the override lever!', 'already_done_text': 'Nothing happens.'})
        # testing will this event work without an item?
        events.insert(31, {'id': 21, 'done': False, 'room': 999, 'item_name': 'bridge door',
                           'first_time_text': 'After the captain stops twitching, the spacesuit emits a series of beeps. Then the bridge door panel lights up. A second later, the door do the bridge slides open.',
                           'already_done_text': 'The door to the bridge is already open.'})
        events.insert(32, {'id': 32, 'done': False, 'room': 44, 'item_name': 'code generator',
                           'first_time_text': 'You press the red button. Random numbers and letters appear quickly then change on the screen. It eventually stops on a short string of characters.',
                           'already_done_text': 'You press the button again, but nothing happens. Must be a one-time thing.'})
        events.insert(33, {'id': 33, 'done': False, 'room': 45, 'item_name': 'override lever',
                           'first_time_text': 'The lever fits nicely into the socket. You pull it down and hear distant machinery grind into action. '
                                              'The lockdown console now reads:\n\t\"NO LOCKDOWN - Offline systems: none',
                           'already_done_text': 'Re-inserting the lever and moving it around has no visible effect on the data displayed.'})
        events.insert(34, {'id': 34, 'done': False, 'room': 21, 'item_name': 'launch controls',
                           'first_time_text': 'You activate the launch controls.',
                           'already_done_text': 'You activate the launch controls.'})
        events.insert(35, {'id': 35, 'done': False, 'room': 22, 'item_name': 'launch console',
                           'first_time_text': 'You activate the launch console.',
                           'already_done_text': 'You activate the launch console.'})
        events.insert(36, {'id': 36, 'done': False, 'room': 999, 'item_name': 'lockbox',
                           'first_time_text': 'You try prying the box open, but it\'s locked. The square keyhole is tiny and shallow. It must require an oddly shaped key.',
                           'already_done_text': 'Still at it? The box is locked. Maybe those symbols mean something?'})
        events.insert(37, {'id': 37, 'done': False, 'room': 999, 'item_name': 'dented tricorder',
                           'first_time_text': 'You scan your surroundings, but all the tricorder does is let out two beeps.',
                           'already_done_text': 'Scanning...beep...beep.'})
        events.insert(38, {'id': 38, 'done': False, 'room': 11, 'item_name': 'retina scanner',
                           'first_time_text': 'You peer into the retina scanner. It lets out a low, disapproving beep.',
                           'already_done_text': 'You move your head so your other eye is scanned. Still nothing.'})
        events.insert(39, {'id': 39, 'done': False, 'room': 999, 'item_name': 'phaser booster',
                           'first_time_text': 'The booster slides nicely onto the phaser. Now you\'re playing with power.',
                           'already_done_text': 'The phaser is already enhanced with the booster.'})
        events.insert(40, {'id': 40, 'done': False, 'room': 999, 'item_name': 'medium stimpack',
                           'first_time_text': 'You stick the medium stimpack into your belly. A warm glow courses from your midsection to your extremities. You feel much better.',
                           'already_done_text': 'The medium stimpack is used up.'})
        events.insert(41, {'id': 41, 'done': False, 'room': 47, 'item_name': 'clogged toilet',
                           'first_time_text': 'It doesn\'t flush, and with all that clothing stuck inside, it seems like a bad idea to use it as designed.',
                           'already_done_text': 'It doesn\'t flush, and with all that clothing stuck inside, it seems like a bad idea to use it as designed.'})
        events.insert(42, {'id': 42, 'done': False, 'room': 47, 'item_name': 'astroplunger',
                           'first_time_text': 'You apply your best plunging technique to the clogged toilet. After a vigorous effort, the you extract a drenched custodial uniform! '
                                              'The waste purification solution is causing it to quickly dissolve, but a key on a ring that was attached to the uniform belt remains.',
                           'already_done_text': 'There isn\'t anything to plunge here.'})
        events.insert(43, {'id': 43, 'done': False, 'room': 48, 'item_name': 'metal key',
                           'first_time_text': 'With a little effort, you are able to unlock the door to the Workroom.',
                           'already_done_text': 'The workroom door is already unlocked.'})
        events.insert(44, {'id': 44, 'done': False, 'room': 49, 'item_name': 'workbench',
                           'first_time_text': 'The workbench by itself doesn\'t do much. Try experimenting with other items. Did you read the directions?',
                           'already_done_text': 'It still doesn\'t do anything. There has to be instructions for this thing.'})
        events.insert(45, {'id': 45, 'done': False, 'room': 999, 'item_name': 'digipad9',
                           'first_time_text': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                                              '\n\tThey\'re hunting the custodial staff. I guess it\'s because we have access to so much of the ship.'
                                              '\n\tSome of the team is hiding their uniforms. I guess the dark blue color gives us away. -B',
                           'already_done_text': 'The digipad reads:'
                                                '\n\tThey\'re hunting the custodial staff. I guess it\'s because we have access to so much of the ship.'
                                                '\n\tSome of the team is hiding their uniforms. I guess the dark blue color gives us away. -B'})
        events.insert(46, {'id': 46, 'done': False, 'room': 999, 'item_name': 'workbench manual',
                           'first_time_text': 'You thumb through the manual.'
                                              '\n\t...Holding high-heat materials requires gloves reinforced with non-conductive fibers...'
                                              '\n\t...A workbench is only as effective as it is clean. Buy our patented Bleakwipes to keep your workspace factory-pure...'
                                              '\n\t...Most levers can be constructed with a bar, a grip for holding, and some kind of tip that will connect to...'
                                              '\n\t...Fuel cell containers are not worth modifying. StarClunk makes the best...',
                           'already_done_text': 'You scan the manual again.'
                                                '\n\t...Holding high-heat materials requires gloves reinforced with non-conductive fibers...'
                                                '\n\t...Most levers can be constructed with a bar, a grip for holding, and some kind of tip that will connect to...'
                                                '\n\t...A workbench is only as effective as it is clean. Buy our patented Bleakwipes to keep your workspace factory-pure...'
                                                '\n\t...Fuel cell containers are not worth modifying. StarClunk makes the best...'})

        creatures.append({'id': 0, 'name': 'Prison guard',
                          'description': 'The guard is 6 feet tall with a sturdy build, greenish skin, and eyes that are cloudy and dark. Its posture is full of anger. No weapons are visible, but its knuckles look pointy.',
                          'room': 1, 'max_hp': 40, 'current_hp': 40, 'is_dead': False, 'is_hostile': False,
                          'status_neutral': 'It isn\'t interested in you.', 'status_hostile': 'It\'s very mad at you.',
                          'damage': 10, 'hit_bonus': 10, 'attack_chance': 65, 'is_fatigued': False, 'death_event': 3,
                          'was_seen': False,
                          'dead_description': 'The lifeless body of the prison guard is a foreboding sight.'})
        creatures.append({'id': 1, 'name': 'Spry zombie',
                          'description': 'This zombified crewmate is short, lithe, and unpredictable. It has that familiar green skin and murky eyes. Blood and bits of flesh are visible on the tips of its fingers.',
                          'room': 30, 'max_hp': 60, 'current_hp': 60, 'is_dead': False, 'is_hostile': True,
                          'status_neutral': 'It isn\'t interested in you.', 'status_hostile': 'It\'s very mad at you.',
                          'damage': 15, 'hit_bonus': 10, 'attack_chance': 70, 'is_fatigued': False, 'death_event': 12,
                          'was_seen': False,
                          'dead_description': 'The zombie looks even smaller now that it\'s dead.'})
        creatures.append({'id': 2, 'name': 'Hulking guard',
                          'description': 'This massive guard is a head taller than you, with milky eyes and a ghoulish complexion. Even though its wide body moves slowly, you sense it holds the force of a great catapult within. '
                                         'It seems preoccupied, looking all around as it licks its lips and chews its own cheek.',
                          'room': 25, 'max_hp': 200, 'current_hp': 200, 'is_dead': False, 'is_hostile': True,
                          'status_neutral': 'It isn\'t interested in you.', 'status_hostile': 'It stares hungrily at you.',
                          'damage': 20, 'hit_bonus': 5, 'attack_chance': 60, 'is_fatigued': False, 'death_event': 21,
                          'was_seen': False,
                          'dead_description': 'The monstrous heap of wasted flesh is unnerving. You are relieved that it\'s dead.'})
        creatures.append({'id': 3, 'name': 'Captain',
                          'description': 'The captain is wearing a spacesuit that offers protection from weapons and the atmosphere. Their helmet has a mirrored visor, but you think you see clear, intense eyes within. '
                                         'The captain holds a particle blaster.',
                          'room': 43, 'max_hp': 100, 'current_hp': 100, 'is_dead': False, 'is_hostile': False,
                          'status_neutral': 'They appear disinterested in you.', 'status_hostile': 'They take aim at you.',
                          'damage': 15, 'hit_bonus': 10, 'attack_chance': 70, 'is_fatigued': False, 'death_event': 31,
                          'was_seen': False,
                          'dead_description': 'The captain\'s spacesuit is badly damaged from the fight, but it isn\'t moving.'})

        # initialize special vars
        special_done.append({'id': 0, 'done': False})
        special_done.append({'id': 1, 'done': False})

        # sets the special event to apply to rooms 5-49
        for i in range(5, 50):
            special_rooms.append(i)

    elif choice == '4':
        safe_rooms = [11, 30, 31, 32, 33]
        starting_room = 0
        exit_room = 2
        player_hp = 100
        intro_text = '*** Welcome to Lake Tortuga ***\n\nYou just got home from school. It was a long day. You aren\'t tired, but you feel a little uneasy. Maybe it\'s the note that someone stuffed in your pocket while you were riding the bus. As you grab for the note, you hear a voice.\n\n\t\'Reveal the note to find your way.\'\n\nStartled, you drop the note onto the floor.\n'
        outro_text = 'You are back at home.\nYour heroism has restored the ecosystem of Lake Tortuga. All creatures, especially the turtles, rejoice.\n\nYou\'ve won the game! Thanks for playing.'
        launch_code = ''

        world.insert(0, {'visible': True, 'name': 'Foyer', 'prefix': 'in the', 'name2': '',
                         'desc': 'This entryway is just inside the front door of your home. Most of the house is accessible from here. The dining room lies to the west, the living room is south, a stairway leads up to the second-level rooms, '
                                 'and a door to the garage is east. On the northern wall is the front door, but some force is keeping it shut.',
                         'exits': {'s': 4, 'w': 1, 'e': 5, 'u':6}})
        world.insert(1, {'visible': True, 'name': 'Dining room', 'prefix': 'in the', 'name2': '',
                         'desc': 'Many happy meals were shared at the table in this room. It connects to the kitchen to the south, and the foyer opens to the east.',
                         'exits': {'s': 3, 'e': 0}})
        world.insert(2,  {'visible': True, 'name': 'Home', 'prefix': 'at', 'name2': '',
                         'desc': 'It feels good to be home.',
                         'exits': {}})
        world.insert(3, {'visible': True, 'name': 'Kitchen', 'prefix': 'in the', 'name2': '',
                         'desc': 'The décor in the kitchen is dated, but functional. The dining room is to the north.',
                         'exits': {'n': 1}})
        world.insert(4, {'visible': True, 'name': 'Living room', 'prefix': 'in the', 'name2': '',
                         'desc': 'This inviting space encourages you to lounge on the plush furniture. The foyer is visible to the north',
                         'exits': {'n': 0}})
        world.insert(5, {'visible': True, 'name': 'Garage', 'prefix': 'in the', 'name2': '',
                         'desc': 'The garage is filled with a musty smell. Tools and spare car parts line the walls. A box of curious junk was spilled across the workbench. The door back into the house is to the west. The door to the outside seems to be jammed.',
                         'exits': {'w': 0}})
        world.insert(6, {'visible': True, 'name': 'Landing', 'prefix': 'on the', 'name2': '',
                         'desc': 'At the top of the stairs is a narrow landing. It leads west to your bedroom, and a door to your parents\' room is south. You can see the foyer at the bottom of the stairs.',
                         'exits': {'w': 7, 's': 8, 'd': 0}})
        world.insert(7, {'visible': True, 'name': 'Bedroom', 'prefix': 'in your', 'name2': '',
                         'desc': 'A small but functional desk, a dresser, and an unmade bed take up space in the dim room. The door to the landing is east.',
                         'exits': {'e': 6}})
        world.insert(8, {'visible': True, 'name': 'Parent\'s bedroom', 'prefix': 'in your', 'name2': '',
                         'desc': 'A large bed dominates the space. On the opposing wall, a wide mirror is hung above a squat dresser. The only exit is to the north.',
                         'exits': {'n': 6}})
        world.insert(9, {'visible': False, 'name': 'Street', 'prefix': 'on the', 'name2': '',
                         'desc': 'A few trees line this quiet single-lane road that winds past your home. Your house is directly south. From the north you can hear the water lap at the shore of the lake.',
                         'exits': {'s': 0, 'n': 10}})
        world.insert(10, {'visible': True, 'name': 'Lakeshore', 'prefix': 'at the', 'name2': '',
                          'desc': 'A rocky, muddy shoreline separates the gently rippling lake water from a path south to the street. To the northeast is a pier that extends into the lake.',
                          'exits': {'s': 9, 'ne': 11}})
        world.insert(11, {'visible': True, 'name': 'Pier', 'prefix': 'on the', 'name2': '',
                          'desc': 'The splintered planks of the pier jut into the murky lake. Rocks, lily pads, and cattails dot the surrounding waters. Dry land is to the southwest.',
                          'exits': {'sw': 10}})
        world.insert(12, {'visible': False, 'name': 'Surface', 'prefix': 'floating on the', 'name2': '',
                          'desc': 'The cool lake water ripples past toward the shore. Through the grainy water, you see a small clearing in the water below. The pier looms a few feet above the water.',
                          'exits': {'d': 13}})
        world.insert(13, {'visible': True, 'name': 'South shallows', 'prefix': 'in the', 'name2': '',
                          'desc': 'As you swim through the water, you see the shallows extend to the east and to the west. A cave network is accessible below. You can see the pier through the water\'s surface above.',
                          'exits': {'e': 14, 'w': 20, 'u': 12, 'd': 21}})
        world.insert(14, {'visible': True, 'name': 'Southeast shallows', 'prefix': 'in the', 'name2': '',
                          'desc': 'You are swimming in shallow water in the southeast corner of the lake. You see clearings to the west and to the north. A large log extends from the sandy bottom up to the surface.',
                          'exits': {'w': 13, 'n': 15, 'u': 30}})
        world.insert(15, {'visible': True, 'name': 'East shallows', 'prefix': 'in the', 'name2': '',
                          'desc': 'Swimming through the shallow water, you see clearings to the north and the south. Below you is another entrance to a craggy tunnel.',
                          'exits': {'n': 16, 's': 14, 'd': 23}})
        world.insert(16, {'visible': True, 'name': 'Northeast shallows', 'prefix': 'in the', 'name2': '',
                          'desc': 'You are swimming in shallow water in the northeast corner of the lake. Clearings are visible to to the south and west. A moss-covered boulder pokes its head out of the water to the surface above.',
                          'exits': {'s': 15, 'w': 17, 'u': 31}})

        # remove access to room 36 after debugging
        world.insert(17, {'visible': True, 'name': 'North shallows', 'prefix': 'in the', 'name2': '',
                          'desc': 'Tall reeds are thick in the northern edge of the lake. As you swim through the water, you see the surface above. A giant clam shell rests on the northern edge of this clearing. It is firmly shut. The shallows extend to the east and to the west. Another cave entrance lies below.',
                          'exits': {'e': 16, 'w': 18, 'd': 25, 'n':36}})
        # remove access to room 36 after debugging

        world.insert(18, {'visible': True, 'name': 'Northwest shallows', 'prefix': 'in the', 'name2': '',
                          'desc': 'The water in the northwest corner of the lake is choked with silt. Clearings are visible to to the south and east. A massive branch from a long-dead tree provides a path up to the water\'s surface above. You almost miss the tiny alcove to the southeast.',
                          'exits': {'s': 19, 'e': 17, 'u': 32, 'se': 42}})
        world.insert(19, {'visible': True, 'name': 'West shallows', 'prefix': 'in the', 'name2': '',
                          'desc': 'As you glide through the shallow water, skirting rocks along the western edge of the lake, you spot clearings to the north and the south. Between a cluster of grim stones below is a narrow opening.',
                          'exits': {'n': 18, 's': 20, 'd': 27}})
        world.insert(20, {'visible': True, 'name': 'Southwest shallows', 'prefix': 'in the', 'name2': '',
                          'desc': 'This section of the lake is especially rocky. Even for you, it takes great concentration to navigate the shallow waters. More open areas of the lake are visible to to the north and east. Between those exits, you spot an opening in the rocks to the northeast. A tall, slender stone runs from the depths below to a flat area just above you.',
                          'exits': {'n': 19, 'e': 13, 'ne': 39, 'u': 33}})
        world.insert(21, {'visible': True, 'name': 'Southern depths', 'prefix': 'in the', 'name2': '',
                          'desc': 'This narrow entryway is a crossroads of underwater tunnels. The cave winds to the northeast and northwest, and opens to the darkness below. A route up to the shallow water of the lake is visible above.',
                          'exits': {'ne': 22, 'nw': 28, 'd': 29, 'u': 13}})
        world.insert(22, {'visible': True, 'name': 'Southeast tunnel', 'prefix': 'in the', 'name2': '',
                          'desc': 'Jagged rocks make up the walls of this tunnel that runs from the southwest to the northeast. An inflated air bladder juts out from the eastern wall. It completely fills an opening that looks big enough for you to swim through.',
                          'exits': {'sw': 21, 'ne': 23}})
        world.insert(23, {'visible': True, 'name': 'Eastern depths', 'prefix': 'in the', 'name2': '',
                          'desc': 'It seems like a little room has been carved into the stone, but the weight of the surrounding rocks makes you uneasy. Fortunately, there are exits to the southwest and northwest. A hole in the center of the cavern leads down to an even darker place. Above you see friendly shallow waters.',
                          'exits': {'sw': 22, 'nw': 24, 'd': 29, 'u': 15}})
        world.insert(24, {'visible': True, 'name': 'Northeast tunnel', 'prefix': 'in the', 'name2': '',
                          'desc': 'You cruise through this smooth, wide tunnel that winds from the southeast to the northwest.',
                          'exits': {'se': 23, 'nw': 25}})
        world.insert(25, {'visible': True, 'name': 'Northern depths', 'prefix': 'in the', 'name2': '',
                          'desc': 'A rough, bent path has been cut through this space, leaving openings to the southwest and southeast. Below is an opening into a darker section of the cave network. A shaft of light streams down from above.',
                          'exits': {'sw': 26, 'se': 24, 'd': 29, 'u': 17}})
        world.insert(26, {'visible': True, 'name': 'Northwest tunnel', 'prefix': 'in the', 'name2': '',
                          'desc': 'You find this plain passageway is a little warmer than the surrounding waters. It opens to the northeast and southwest.',
                          'exits': {'ne': 25, 'sw': 27}})
        world.insert(27, {'visible': True, 'name': 'Western depths', 'prefix': 'in the', 'name2': '',
                          'desc': 'The water in this space is thick with small debris, making it hard to see. You feel that the cavern bends like an elbow leading to tunnels to the northeast and southeast. Greater darkness and a slight current are pulling you downward. You see the shallow, clearer waters of the lake above you.',
                          'exits': {'ne': 26, 'se': 28, 'd': 29, 'u': 19}})
        world.insert(28, {'visible': True, 'name': 'Southwest tunnel', 'prefix': 'in the', 'name2': '',
                          'desc': 'This cramped passage runs in a northwest-to-southeast direction. To the southwest you see an opening you could swim through.',
                          'exits': {'nw': 27, 'se': 21, 'sw': 41}})
        world.insert(29, {'visible': True, 'name': 'Cave center', 'prefix': 'in the', 'name2': '',
                          'desc': 'This circular room feels like the inside of a well. Passageways out are high on the northern, southern, eastern, and western sides of the space. At the bottom is a bulky, round door made of rotted wood. Somehow a darkness seeps through the cracks of the door.',
                          'exits': {'n': 25, 's': 21, 'e': 23, 'w': 27, 'd': 34}})
        world.insert(30, {'visible': True, 'name': 'Sun-blanched log', 'prefix': 'on a', 'name2': '',
                          'desc': 'The bark of this wide log is somehow intact. It serves as a comfortable surface when in direct sunlight. You can follow the log back down into the water.',
                          'exits': {'d': 14}})
        world.insert(31, {'visible': True, 'name': 'Warm boulder', 'prefix': 'on a', 'name2': '',
                          'desc': 'The rockface that sticks out of the water is dry and bedded with spongy moss. You can scale the boulder back down into the water.',
                          'exits': {'d': 16}})
        world.insert(32, {'visible': True, 'name': 'Dead branch', 'prefix': 'on a', 'name2': '',
                          'desc': 'Several crooks in this partially submerged branch can be nestled into. The leaves are long-gone, leaving the you exposed to the open sky. You can follow the branch back down into the shallow water.',
                          'exits': {'d': 18}})
        world.insert(33, {'visible': True, 'name': 'Stony mini-mesa', 'prefix': 'on a', 'name2': '',
                          'desc': 'This rock outcropping feels like the top of a desert butte, though it is surrounded by water. Just head back down the stone to re-enter the shallow lake.',
                          'exits': {'d': 20}})
        world.insert(34, {'visible': True, 'name': 'Antechamber', 'prefix': 'in the', 'name2': '',
                          'desc': 'Glowing creepy-crawlies provide the only light in this unfriendly pit. The way back to the well is above. A hollow dread pulls at you from the room to the south.',
                          'exits': {'u': 29, 's': 35}})
        world.insert(35, {'visible': True, 'name': 'Slimy core', 'prefix': 'in the', 'name2': '',
                          'desc': 'This wide cavern seems impossibly large. It must extend deep into the earth. Morose stone and decayed roots line the walls. The only exit is to the north. A circular hole has been bored into the eastern wall, near the floor. It is too small get into.',
                          'exits': {'n': 34}})
        world.insert(36, {'visible': False, 'name': 'Mermaid\'s grotto', 'prefix': 'in the', 'name2': '',
                          'desc': 'The low ceiling of this deep recess makes you feel closed-in. Seashells cover the floor. There is a small door to the south.',
                          'exits': {'s': 17}})
        world.insert(37, {'visible': True, 'name': 'Industrial pipe', 'prefix': 'in the', 'name2': '',
                          'desc': 'The entire surface of this cylindrical tube is covered in a green substance. If you focus on it, the surface seems to pulsate slowly. There is a grate on the east end, but enough of it has been worn, or eaten, away for you to proceed. The west end of the pipe leads back to the cave.',
                          'exits': {'e': 38, 'w': 22}})
        world.insert(38, {'visible': True, 'name': 'Tank room', 'prefix': 'in the', 'name2': '',
                          'desc': 'It seems like you are inside a voluminous, decay'
                                  'ing tank. Mechanical filters are choked with dark green mossy fibers. Wispy tendrils undulate from the ceiling and walls. The pipe that brought you into this place is to the west.',
                          'exits': {'w': 37}})
        world.insert(39, {'visible': True, 'name': 'Rocky passage', 'prefix': 'in a', 'name2': '',
                          'desc': 'This rough-hewn throughway appears to be carved by unnatural forces. It is a T-intersection. You can swim to the north, northeast, and southwest.',
                          'exits': {'n': 40, 'ne': 41, 'sw': 20}})
        world.insert(40, {'visible': True, 'name': 'Murky chamber', 'prefix': 'in the', 'name2': '',
                          'desc': 'A pile of rocks fills a corner of the room, mounting up to the ceiling and possibly beyond. You can\'t go that way, but a rope extends through the opening. It is connected to a large cage resting on the floor. A gentle current flows through this room, from the south to the east.',
                          'exits': {'s': 39, 'e': 41}})
        world.insert(41, {'visible': True, 'name': 'Twisty tunnel', 'prefix': 'in a', 'name2': '',
                          'desc': 'Something must have carved through the rock to make this jagged path. The ways out are to the west, northeast, and southwest.',
                          'exits': {'w': 40, 'ne': 28, 'sw': 39}})
        world.insert(42, {'visible': True, 'name': 'Curious alcove', 'prefix': 'in a', 'name2': '',
                          'desc': 'This small room was hollowed out from the nearby rocks. The water is thick with particles, but you see an ancient stone fountain connected to the eastern wall. You can leave the alcove by heading northwest.',
                          'exits': {'nw': 18}})
        world.insert(43,
                     {'visible': False, 'name': 'Nether', 'prefix': 'in the', 'name2': '', 'desc': 'You are nowhere.',
                      'exits': {}})

                      # hammer weapon is put in the nether, an unused room - seems to fix claws attack bug
        things.append({'name': 'hammer', 'prefix': 'a',
                       'description': 'It\'s a classic ball-peen hammer. Could do some real damage.', 'location': 43,
                       'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': 10, 'damage': 30, 'hit_bonus': 20, 'no_drop': False})
        things.append({'name': 'faded note', 'prefix': 'a',
                       'description': 'After you smooth out the crumpled note, you see faint writing on the left half of the page. It reads:\n\n\t\'Our lake has been overtaken by\n\t This creature of the sea has\n\t Only the one who wears the rin\n\t The one who bears symbols of\n\t Peril now fills the lake. If y\n\t Find the guardians, remove th', 'location': 0,
                       'on_person': False, 'moveable': True, 'is_weapon': False, 'base_damage': 0, 'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'hex nut', 'prefix': 'a', 'description': 'This sturdy piece of steel has a threaded hole in the middle. The six-sided shape feels familiar.',
                       'location': 5, 'on_person': False, 'moveable': True, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'shirt', 'prefix': 'a',
                       'description': 'This dark navy T-shirt has an image of the powerful band of heroes, the Teenage Mutant Ninja Turtles.',
                       'location': 7, 'on_person': False, 'moveable': True, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'kitchen sink', 'prefix': 'the',
                       'description': 'A few dishes and forks with caked-on egg are all that remain from this morning\'s breakfast. A gleaming water droplet trembles at the lip of the faucet.',
                       'location': 3, 'on_person': False, 'moveable': False, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'filter', 'prefix': 'a',
                       'description': 'The short metallic tube looks like it would fit on a water faucet. There\'s a faded, turtle-shell pattern covering the filter.',
                       'location': 5, 'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'claws', 'prefix': 'your', 'description': 'Careful with those things. They look pointy!',
                       'location': 12,
                       'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': 10, 'damage': 30,
                       'hit_bonus': 30, 'no_drop': True})
        things.append({'name': 'shell button', 'prefix': 'a',
                       'description': 'Sticking out from the wall is an ivory-colored shell. It looks like you could push it.',
                       'location': 39, 'on_person': False, 'moveable': False, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'snail shell', 'prefix': 'a',
                       'description': 'The empty snail shell is dark brown in color, blending into the rock it rests on. It can\'t be picked up, but it seems to have some give when pressed.',
                       'location': 15, 'on_person': False, 'moveable': False, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'conch', 'prefix': 'a',
                       'description': 'The swirling pattern of this conical shell is mesmerizing. It is loosely wedged into the side of the passageway.',
                       'location': 26, 'on_person': False, 'moveable': False, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'duckweed', 'prefix': 'some',
                       'description': 'These bright green water lentils look like they could be a healthy snack.',
                       'location': 19, 'on_person': False, 'moveable': True, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'lake lettuce', 'prefix': 'some',
                       'description': 'It\'s a marvel that such a succulent plant could grow in these murky waters. The leafy mass seems like it could restore your strength.',
                       'location': 21, 'on_person': False, 'moveable': True, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'water grubs', 'prefix': 'some',
                       'description': 'If they weren\'t slimy, hairy, and wriggling, these beetle larvae might be cute. Never mind that--you\'re more interested in the tasty protein they provide.',
                       'location': 24, 'on_person': False, 'moveable': True, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'air bladder', 'prefix': 'an',
                       'description': 'The massive balloon that blocks the way east is made of high-grade industrial rubber. It looks like it could be popped, but your claws aren\'t sharp enough.',
                       'location': 22, 'on_person': False, 'moveable': False, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'fountain', 'prefix': 'the',
                       'description': 'Although you\'re already in the lake, a jet of pure water springs from this fountain. It cuts through the surrounding filth.',
                       'location': 42, 'on_person': False, 'moveable': False, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'lobster trap', 'prefix': 'a',
                       'description': 'Distressed wood and rusted wire are fashioned into a large cage. Tied to the top is the rope that leads through the opening above. An enormous crayfish with a burnt umber carapace is coiled within the trap. It does not look happy. A worn lock is all that keeps its deadly pincers at bay.',
                       'location': 40, 'on_person': False, 'moveable': False, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'shell', 'prefix': 'your', 'description': 'Your shell is a beautiful dome of protection. Use it for the perfect defense.',
                       'location': 12,
                       'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': -999, 'damage': -999,
                       'hit_bonus': -999, 'no_drop': True})
        things.append({'name': 'remote', 'prefix': 'the',
                       'description': 'The remote controller looks like it could operate any of the video and audio devices in the house. Unfortunately, it needs two AA batteries to work.',
                       'location': 4, 'on_person': False, 'moveable': True, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'batteries', 'prefix': 'the',
                       'description': 'The two C batteries look like they have plenty of charge.', 'location': 5,
                       'on_person': False, 'moveable': True, 'is_weapon': False, 'base_damage': 0, 'damage': 0,
                       'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'leather boot', 'prefix': 'a',
                       'description': 'There are no laces in the sodden boot. Its tongue flops around in defeat.',
                       'location': 28, 'on_person': False, 'moveable': True, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'wild celery', 'prefix': 'the',
                       'description': 'Long ribbon-like leaves spiral upward from the bottom of the lake.',
                       'location': 14, 'on_person': False, 'moveable': False, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})
        things.append({'name': 'clam shell', 'prefix': 'the',
                       'description': 'The enormous rigid shell is impenetrable, wih ridges that make you think of giant waves. It\'s so big that you can\'t see around it. Some say a clam is nature\'s zipper.',
                       'location': 17, 'on_person': False, 'moveable': False, 'is_weapon': False, 'base_damage': 0,
                       'damage': 0, 'hit_bonus': 0, 'no_drop': False})

        # note 999 event needs to come AFTER (in terms of index) room-specific event
        events.insert(0, {'id': 0, 'done': False, 'room': 3, 'item_name': 'filter',
                          'first_time_text': 'You screw the filter onto the faucet, making a marked improvement. Maybe it\'s just the light, but it seems to glow slightly.',
                          'already_done_text': 'It looks perfect where it is. There\'s nothing more to do with it.'})
        events.insert(1, {'id': 1, 'done': False, 'room': 3, 'item_name': 'enhanced faucet',
                          'first_time_text': 'A stream of clear light pours from the faucet. You are compelled to put the faded note under the gentle flow, and when you do, letters begin to take shape on the blank part of the page!\n\nFrom the front of the house, you hear a strange \'pop,\' or maybe a \'zap?\' You didn\'t notice it before, but the air feels like it is flowing freely again.',
                          'already_done_text': 'A soothing stream of water splashes into the sink.'})
        events.insert(2, {'id': 2, 'done': False, 'room': 999, 'item_name': 'shirt',
                          'first_time_text': 'The T-shirt fits perfectly. You feel invincible.',
                          'already_done_text': 'The T-shirt fits perfectly. You feel invincible.'})
        events.insert(3, {'id': 3, 'done': False, 'room': 11, 'item_name': 'hex nut',
                           'first_time_text': 'Standing at the water\'s edge, wearing the Teenage Mutant Ninja Turtles shirt, the hex nut transforms into a ring. This metallic band fits snugly on your right index finger. '
                                              'You\'ve made the RING OF POWER! You cannot remove the ring, but with it you can now descend into the lake!', 'already_done_text': 'Nothing happens.'})
        events.insert(12, {'id': 12, 'done': False, 'room': 999, 'item_name': 'trident',
                          'first_time_text': 'As the mermaid becomes still, she drops the fearsome trident.',
                          'already_done_text': 'You poke the trident into the air.'})
        events.insert(4, {'id': 4, 'done': False, 'room': 22, 'item_name': 'trident',
                           'first_time_text': 'You jab the pointy end of the trident into the bladder. It pierces the thick material causing air bubbles to rush out and escape towards the surface. As the bladder deflates, you see a round opening to the east!',
                           'already_done_text': 'You poke the trident into the air.'})
        events.insert(5, {'id': 5, 'done': False, 'room': 999, 'item_name': 'claws',
                          'first_time_text': 'You slash with your claws.', 'already_done_text': 'You slash with your claws.'})
        events.insert(6, {'id': 6, 'done': False, 'room': 39, 'item_name': 'shell button',
                          'first_time_text': 'You push the shell into the wall.',
                          'already_done_text': 'The shell is already pressed into the wall.'})
        events.insert(7, {'id': 7, 'done': False, 'room': 15, 'item_name': 'snail shell',
                          'first_time_text': 'You push the snail shell into the rock. It is surprisingly sturdy for something that looks delicate.',
                          'already_done_text': 'The snail shell is already depressed into the rock.'})
        events.insert(8, {'id': 8, 'done': False, 'room': 26, 'item_name': 'conch',
                          'first_time_text': 'The conch slides deeper into the wall.',
                          'already_done_text': 'Only the tip of the conch is accessible. You can\'t push it farther in or remove it.'})
        events.insert(9, {'id': 9, 'done': False, 'room': 999, 'item_name': 'duckweed',
                          'first_time_text': 'You shove a clawful of duckweed into your mouth. A current of strength flows through your body, and you feel better.',
                          'already_done_text': 'The duckweed served its purpose.'})
        events.insert(10, {'id': 10, 'done': False, 'room': 999, 'item_name': 'lake lettuce',
                          'first_time_text': 'The broad leaves of lake lettuce are surprisingly flavorful. With each bite, you feel your aches and wounds fade.',
                          'already_done_text': 'The lake lettuce was delicious.'})
        events.insert(11, {'id': 11, 'done': False, 'room': 999, 'item_name': 'water grubs',
                          'first_time_text': 'Those squirmy suckers know what\'s about to happen. You pop them into your mouth one by one. Each one oozes like a jelly donut as you start munching. It\'s invigorating.',
                          'already_done_text': 'The water grubs were so satisfying.'})
        events.insert(13, {'id': 13, 'done': False, 'room': 42, 'item_name': 'curious blob',
                           'first_time_text': 'You hold the blob under the current of clean water flowing from the fountain. The yellowish shape breaks apart, leaving you with a rusty key!',
                           'already_done_text': 'It is no longer a blob.'})
        events.insert(14, {'id': 14, 'done': False, 'room': 999, 'item_name': 'curious blob',
                           'first_time_text': 'With that final swipe, the algae begins disintegrating. It was concealing a dark yellow blob that hangs suspended in the water. ',
                           'already_done_text': 'Not sure how you\'re supposed to use that.'})
        events.insert(15, {'id': 15, 'done': False, 'room': 42, 'item_name': 'fountain',
                          'first_time_text': 'You hold the blob under the current of clean water flowing from the fountain. The yellowish shape breaks apart, leaving you with a rusty key!',
                          'already_done_text': 'You hold your claws under the cleansing stream. Feels nice.'})
        events.insert(16, {'id': 16, 'done': False, 'room': 40, 'item_name': 'rusty key',
                          'first_time_text': 'With some effort, you are able to fit the rusty key into the lock on the cage. You turn the key, and the lock falls apart. The crayfish senses the opportunity and bursts from the trap!',
                          'already_done_text': 'The cage is unlocked.'})
        events.insert(17, {'id': 17, 'done': False, 'room': 999, 'item_name': 'none',
                           'first_time_text': 'After you deliver the killing blow, the crayfish shudders and extends its pincers towards you. A crack like a thunder peal reverberates through the water, and the deadly pincers break off the crayfish\'s forelimbs.',
                           'already_done_text': 'You fit the pincers over your claws.'})
        events.insert(18, {'id': 18, 'done': False, 'room': 999, 'item_name': 'pincers',
                          'first_time_text': 'You snap your powerful pincers.', 'already_done_text': 'You snap your powerful pincers.'})
        events.insert(19, {'id': 19, 'done': False, 'room': 999, 'item_name': 'broken pincers',
                          'first_time_text': 'You fit the pincers over your claws.', 'already_done_text': 'You fit the pincers over your claws.'})
        events.insert(20, {'id': 20, 'done': False, 'room': 999, 'item_name': 'none',
                           'first_time_text': 'With your final deadly snip, you sever the body of the sea serpent. A large sapphire falls out of the its belly. You hear a voice from within,\n\n\t\'Take the Gem of restoration. When you are ready, use it to return to the land above.\'',
                            'already_done_text': 'Your death blow produced the gem.'})
        events.insert(21, {'id': 21, 'done': False, 'room': 999, 'item_name': 'gem of restoration',
                           'first_time_text': 'As you concentrate while clutching the gem, you feel the might of turtle power ebb from your being. You return to your human form, and find yourself transported to a safe, dry place.',
                           'already_done_text': 'You already used the gem.'})
        events.insert(22, {'id': 22, 'done': False, 'room': 999, 'item_name': 'faded note',
                           'first_time_text': 'You try to make sense of the partial text on the once-crumpled note. It reads:\n\n\t\'Our lake has been overtaken by\n\t This creature of the sea has\n\t Only the one who wears the rin\n\t The one who bears symbols of\n\t Peril now fills the lake. If y\n\t Find the guardians, remove th',
                           'already_done_text': 'You try to make sense of the partial text on the once-crumpled note. It reads:\n\n\t\'Our lake has been overtaken by\n\t This creature of the sea has\n\t Only the one who wears the rin\n\t The one who bears symbols of\n\t Peril now fills the lake. If y\n\t Find the guardians, remove th'})
        events.insert(23, {'id': 23, 'done': False, 'room': 999, 'item_name': 'note',
                           'first_time_text': 'You read the note:\n\n\t\'Our lake has been overtaken by a venomous tyrant.\n\t This creature of the sea has corrupted the waters and installed three hidden guardians.\n\t Only the one who wears the ring of power may enter the lake and save it.\n\t The one who bears symbols of great warriors can forge the ring at the water\'s edge.\n\t Peril now fills the lake. If you can emerge, even for a moment, you may find relief, or more danger.\n\t Find the guardians, remove them, and face the usurper. Purge this being from the lake to redeem it.\'',
                           'already_done_text': 'You read the note:It now reads:\n\n\t\'Our lake has been overtaken by a venomous tyrant.\n\t This creature of the sea has corrupted the waters and installed three hidden guardians.\n\t Only the one who wears the ring of power may enter the lake and save it.\n\t The one who bears symbols of great warriors can forge the ring at the water\'s edge.\n\t Peril now fills the lake. If you can emerge, even for a moment, you may find relief, or more danger.\n\t Find the guardians, remove them, and face the usurper. Purge this being from the lake to redeem it.\''})
        events.insert(24, {'id': 24, 'done': False, 'room': 3, 'item_name': 'kitchen sink',
                          'first_time_text': 'You turn the faucet on and off. The miracle of indoor plumbing.',
                          'already_done_text': 'You let the water run over your hands. Feels nice.'})
        events.insert(25, {'id': 25, 'done': False, 'room': 999, 'item_name': 'shell',
                          'first_time_text': 'You pull your limbs and head deep into your shell.', 'already_done_text': 'You pull your limbs and head deep into your shell.'})
        events.insert(26, {'id': 26, 'done': False, 'room': 999, 'item_name': 'remote',
                          'first_time_text': 'You point the remote and press its buttons. Without batteries, it doesn\'t do anything.', 'already_done_text': 'The remote is useless without two AA batteries.'})
        events.insert(27, {'id': 27, 'done': False, 'room': 999, 'item_name': 'batteries',
                          'first_time_text': 'You try to find a use for the C batteries, but nothing seems to need them.', 'already_done_text': 'Does anything even use C batteries?'})
        events.insert(28, {'id': 28, 'done': False, 'room': 999, 'item_name': 'leather boot',
                          'first_time_text': 'Back when you had human feet, this boot might have fit you. Now it\'s just ridiculous.', 'already_done_text': 'Without it\'s pair, this mushy boot is just sad.'})
        events.insert(29, {'id': 29, 'done': False, 'room': 999, 'item_name': 'wild celery',
                          'first_time_text': 'All you can do is swim around and through its curly stalks.', 'already_done_text': 'There\'s not much else you can do with it besides admire how peaceful it is.'})
        events.insert(30, {'id': 30, 'done': False, 'room': 17, 'item_name': 'clam shell',
                          'first_time_text': 'With all your might, you try to pry open the shell. Not gonna happen.', 'already_done_text': 'Though it is closed now, something tells you there\'s a way to open the shell.'})

#        # hammer weapon event is included - seems to fix claws attack bug
#        events.insert(6, {'id': 6, 'done': False, 'room': 999, 'item_name': 'hammer',
#                          'first_time_text': 'You swing the hammer.', 'already_done_text': 'You swing the hammer.'})

        creatures.append({'id': 0, 'name': 'Mermaid',
                          'description': 'The mermaid floats with such grace, it is almost hypnotic. She carries a glorious trident.',
                          'room': 36, 'max_hp': 100, 'current_hp': 100, 'is_dead': False, 'is_hostile': False,
                          'status_neutral': 'She isn\'t interested in you, but she eyes you warily.', 'status_hostile': 'She\'s very mad at you.',
                          'damage': 10, 'hit_bonus': 10, 'attack_chance': 70, 'is_fatigued': False, 'death_event': 12, 'was_seen': False,
                          'dead_description': 'The mermaid\'s lifeless body is elegant even in death.' })
        creatures.append({'id': 1, 'name': 'Algae',
                          'description': 'The blob of algae pulses slowly. A green-gray pattern swirls across and through its amoeba-like body.',
                          'room': 38, 'max_hp': 100, 'current_hp': 100, 'is_dead': False, 'is_hostile': False,
                          'status_neutral': 'A menacing energy flows through it.', 'status_hostile': 'It has shifted into an aggressive shape.',
                          'damage': 5, 'hit_bonus': 15, 'attack_chance': 65, 'is_fatigued': False, 'death_event': 14, 'was_seen': False,
                          'dead_description': 'Bits of algae hang in the water, an ominous reminder of the potent creature.' })

        special_rooms.append(12)
        # sets the special event to apply to rooms 13-33
        for i in range(13, 34):
            special_rooms.append(i)

        # initialize special vars
        special_done.append({'id': 0, 'done': False}) # transformation message + claws + shell


def initialize_engine():
    global allowed_moves
    global allowed_actions
    global inventory_quantity
    global room_has_items
    global room_has_mobs
    global locale_visited
    global available_games
    global special_rooms
    global special_done
    global verbose_mode
    allowed_moves = ['n', 'north', 's', 'south', 'e', 'east', 'w', 'west', 'u', 'up', 'd', 'down', 'ne', 'northeast',
                     'nw', 'northwest', 'se', 'southeast', 'sw', 'southwest']
    allowed_actions = ['l', 'look', 'x', 'examine', 'use', 'take', 'drop', 'i', 'inv', 'inventory', '?', 'help', 'quit', 'h',
                       'health', 'r', 'repeat', 'v', 'verbose', 'save', 'load']
    inventory_quantity = 0
    room_has_items = False
    room_has_mobs = False
    locale_visited = False
    available_games = ['1', '2', '3', '4']
    special_rooms = []
    special_done = []
    verbose_mode = True
    # saved_data = {}

def select_game():
    global available_games
    print('Choose a text game by number:')
    print('1 - OG Portal')
    print('2 - Combat practice')
    print('3 - Space adventure')
    print('4 - Lake Tortuga')
    print('If you want to continue a saved game, select the game by number then type \'load\'.')

    game_choice = input('Your choice? ')
    while game_choice not in available_games:
        print('Enter a number from the above list to choose a text game.')
        game_choice = input()
    return game_choice


# main code starts here
initialize_engine()
print('Welcome to TextGames!')
print('')
game_choice = select_game()
load_game(game_choice)
print('')

room = starting_room
show_intro()
last_move = ''
while room != exit_room:
    remove_creature_fatigue(room)

    if player_hp <= 0:
        print('Thanks for playing!')
        print('')
        input('Press ENTER to continue... ')
        break
    if not locale_visited:
        locale(room)
        locale_visited = True
    # repeating check if player dies as a result of special
    if player_hp <= 0:
        print('\nThanks for playing!')
        print('')
        input('Press ENTER to continue... ')
        break

    #moved to locale(room) so it does not occur with every move, just once per new room
    #if room in special_rooms:
        #do_special(room)


    move = get_move()
    if move == "" or move == '' or move is None:
        pass
    elif move == '?' or move == 'help':
        show_help()
    elif move == 'l' or move == 'look':
        look_around(room)
    elif move == 'x' or move == 'examine':
        examine_item(room)
    elif move == 'v' or move == 'verbose':
        toggle_verbose()
    elif move == 'save':
        save_game()
    elif move == 'load':
        load_saved_game()
    elif move == 'use':
        use_item(room)
    elif move == 'take':
        take_item(room)
        creature_attack(room)
    elif move == 'drop':
        drop_item(room)
        creature_attack(room)
    elif move == 'i' or move == 'inv' or move == 'inventory':
        show_inventory(inventory_quantity)
    elif move == 'h' or move == 'health':
        player_wellness(player_hp, 100)
    elif move == 'quit':
        print('Are you sure you want to quit?')
        quit_confirm = input()
        if quit_confirm.lower() == 'y' or quit_confirm.lower() == 'yes':
            print('Thanks for playing!')
            print('')
            input('Press ENTER to continue... ')
            break
        else:
            print('Okay, back to it.')
    else:
        dir = short_move(move)
        if valid_move(room, dir):
            new_room = world[room]['exits'][dir]
            creature_follow(room, new_room)
            room = new_room
            locale_visited = False
        else:
            if move.lower() == 'r' or move.lower() == 'repeat':
                pass
            else:
                print('You can\'t go that way.')
        last_move = move
    print('')

if room == exit_room:
    print(outro_text)
    print('')
    input('Press ENTER to continue... ')