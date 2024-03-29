#! python3
# text_games
# version 1.3.5
# description: added items, creature, events to detention level


# imports
import random


# functions
def locale(current_room):
    print('You are ' + world[current_room]['prefix'] + ' ' + world[current_room]['name'] + '.')
    print(world[current_room]['desc'])
    show_things(current_room)
    show_creatures(current_room)


def look_around(current_room):
    print('You are ' + world[current_room]['prefix'] + ' ' + world[current_room]['name'] + '.')
    print(world[current_room]['desc'])
    show_exits(current_room)
    show_things(current_room)
    show_creatures(current_room)


def examine_item(current_room):
    global inventory_quantity
    global room_has_items
    global room_has_mobs
    global target

    update_things_in_room(current_room)
    if target in available_targets(current_room):
        for thing in things:
            if thing['name'].lower() == target.lower():
                print(thing['description'])
                return

    if room_has_mobs:
        for mob in creatures:
            if mob['room'] == current_room and mob['name'].lower() == target:
                print(
                    mob['description'] + ' ' + mob['name'] + ' ' + creature_wellness(mob['current_hp'], mob['max_hp']),
                    end='')
                if mob['is_dead'] == True:
                    print()
                elif mob['is_hostile'] == False:
                    print(' ' + mob['status_neutral'])
                else:
                    print(' ' + mob['status_hostile'])
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
                if (thing['location'] == current_room and thing['on_person'] == False):
                    print(thing['name'].capitalize())
                    available_choices.append(thing['name'].lower())
        if inventory_quantity > 0:
            for thing in things:
                if (thing['on_person'] == True):
                    print(thing['name'].capitalize())
                    available_choices.append(thing['name'].lower())
        print('What do you want to examine? (type the name or press ENTER for none)')
        choice = input().lower()
        if choice == '':
            return
        while choice not in available_choices:
            print('That\'s not a valid choice. Try again.')
            print('What do you want to examine? (type the name or press ENTER for none)')
            choice = input().lower()
            if choice == '':
                return
        for thing in things:
            if thing['name'].lower() == choice:
                print(thing['description'])
        for mob in creatures:
            if mob['name'].lower() == choice:
                print(
                    mob['description'] + ' ' + mob['name'] + ' ' + creature_wellness(mob['current_hp'], mob['max_hp']),
                    end='')
                if mob['is_dead'] == True:
                    print()
                elif mob['is_hostile'] == False:
                    print(' ' + mob['status_neutral'])
                else:
                    print(' ' + mob['status_hostile'])
    else:
        print('There isn\'t anything to examine here. Go find something!')


def creature_wellness(current, max):
    percentage = current / max * 100
    if percentage > 75:
        return "is in good shape."
    elif percentage > 50:
        return "appears to be in pain."
    elif percentage > 25:
        return "is hurting but still dangerous."
    elif percentage > 0:
        return "is seriously wounded."
    else:
        return "is dead."


def show_creatures(current_room):
    global room_has_mobs
    room_has_mobs = False
    for mob in creatures:
        if mob['room'] == current_room:
            if mob['is_dead'] == False:
                if mob['is_hostile'] == False:
                    print(mob['name'] + ' is here. ' + mob['status_neutral'])
                else:
                    print(mob['name'] + ' is here. ' + mob['status_hostile'])
            else:
                print(mob['name'] + ' is here, but it\'s dead.')
            room_has_mobs = True


def show_things(current_room):
    global room_has_items
    visible_items = 0
    print('Visible items:')
    for thing in things:
        if (thing['location'] == current_room and thing['on_person'] == False):
            print(thing['prefix'].capitalize() + ' ' + thing['name'])
            visible_items = visible_items + 1
            room_has_items = True
    if visible_items == 0:
        print('You don\'t see anything special.')
        room_has_items = False


def update_things_in_room(current_room):
    global room_has_items
    global room_has_mobs
    visible_items = 0
    for thing in things:
        if (thing['location'] == current_room and thing['on_person'] == False):
            visible_items = visible_items + 1
            room_has_items = True
    if room_has_mobs:
        for mob in creatures:
            if (mob['room'] == current_room and mob['name'].lower() == target):
                visible_items = visible_items + 1
                room_has_items = True

    if visible_items == 0:
        room_has_items = False


def show_inventory(quantity):
    if quantity > 0:
        print('You are carrying:')
        for thing in things:
            if thing['on_person'] == True:
                print(thing['prefix'].capitalize() + ' ' + thing['name'])
    else:
        print('You aren\'t carrying anything.')


def take_item(current_room):
    global inventory_quantity
    global room_has_items
    global target
    update_things_in_room(current_room)

    if room_has_items:
        available_choices = []
        for thing in things:
            if (thing['location'] == current_room and thing['on_person'] == False):
                available_choices.append(thing['name'].lower())
        for thing in things:
            if thing['name'].lower() == target.lower():
                if thing['moveable'] == True:
                    thing['on_person'] = True
                    inventory_quantity = inventory_quantity + 1
                    # old print('You pick up ' + thing['prefix'] + ' ' + thing['name'] + '.')
                    print('You pick up the ' + thing['name'] + '.')
                    return
                else:
                    # old print('You can\'t take ' + thing['prefix'] + ' ' + thing['name'] + '.')
                    print('You can\'t take the ' + thing['name'] + '.')
                    return

        print('Items you see:')
        for thing in range(len(available_choices)):
            print(available_choices[thing].capitalize())
        print('What item do you want to take? (type the item name or press ENTER for none)')
        choice = input().lower()
        if choice == '':
            return
        while choice not in available_choices:
            print('That\'s not a valid choice. Try again.')
            print('What item do you want to take? (type the item name or press ENTER for none)')
            choice = input().lower()
            if choice == '':
                return
        for thing in things:
            if thing['name'].lower() == choice:
                if thing['moveable'] == True:
                    thing['on_person'] = True
                    inventory_quantity = inventory_quantity + 1
                    print('You pick up the ' + thing['name'] + '.')
                    # old print('You pick up ' + thing['prefix'] + ' ' + thing['name'] + '.')
                else:
                    print('You can\'t take the ' + thing['name'] + '.')
                    # old print('You can\'t take ' + thing['prefix'] + ' ' + thing['name'] + '.')
    else:
        print('There aren\'t any items worth taking.')


def drop_item(current_room):
    global inventory_quantity
    global target

    if inventory_quantity == 0:
        print('You aren\'t carrying anything.')
        return

    update_things_in_room(current_room)
    if target != '':
        if target in available_targets(current_room):
            for thing in things:
                if thing['name'].lower() == target.lower():
                    thing['on_person'] = False
                    thing['location'] = current_room
                    user_has_items = True
                    print('You drop the ' + thing['name'] + '.')
                    # old print('You drop ' + thing['prefix'] + ' ' + thing['name'] + '.')
                    inventory_quantity = inventory_quantity - 1
            return
        else:
            print('\"' + target + '\" is not in your inventory.')

    if inventory_quantity > 0:
        available_choices = []
        print('Items you are carrying:')
        for thing in things:
            if (thing['on_person'] == True):
                print(thing['name'].capitalize())
                available_choices.append(thing['name'].lower())
        print('What item do you want to drop? (type the item name or press ENTER for none)')
        choice = input().lower()
        if choice == '':
            return
        while choice not in available_choices:
            print('That\'s not a valid choice. Try again.')
            print('What item do you want to drop? (type the item name or press ENTER for none)')
            choice = input().lower()
            if choice == '':
                return
        for thing in things:
            if thing['name'].lower() == choice:
                thing['on_person'] = False
                thing['location'] = current_room
                user_has_items = True
                print('You drop the ' + thing['name'] + '.')
                # old print('You drop ' + thing['prefix'] + ' ' + thing['name'] + '.')
                inventory_quantity = inventory_quantity - 1
    else:
        print('You aren\'t carrying anything.')


def use_item(current_room):
    global inventory_quantity
    global room_has_items
    global target

    update_things_in_room(current_room)
    if target != '':
        if target in available_targets(current_room):
            if weapon_checker(target) == True:
                pick_up_if_weapon(target)
                if attack_checker(current_room):
                    check_event(current_room, target)
                    player_attack(current_room, target)
                else:
                    check_event(current_room, target)
            else:
                check_event(current_room, target)
            creature_attack(current_room)

            return
        else:
            print('\"' + target + '\" is not available to use.')

    if room_has_items or inventory_quantity > 0:
        available_choices = []
        print('Items you can use:')
        if room_has_items:
            for thing in things:
                if (thing['location'] == current_room and thing['on_person'] == False):
                    print(thing['name'].capitalize())
                    available_choices.append(thing['name'].lower())
        if inventory_quantity > 0:
            for thing in things:
                if (thing['on_person'] == True):
                    print(thing['name'].capitalize())
                    available_choices.append(thing['name'].lower())
        print('What item do you want to use? (type the item name or press ENTER for none)')
        choice = input().lower()
        if choice == '':
            return
        while choice not in available_choices:
            print('That\'s not a valid choice. Try again.')
            print('What item do you want to use? (type the item name or press ENTER for none)')
            choice = input().lower()
            if choice == '':
                return

        if weapon_checker(choice) == True:
            pick_up_if_weapon(choice)
            if attack_checker(current_room):
                check_event(current_room, choice)
                player_attack(current_room, choice)
            else:
                check_event(current_room, choice)
        else:
            check_event(current_room, choice)
        creature_attack(current_room)
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
                    if (random.randrange(1, 100) + thing['hit_bonus']) > 50:
                        damage = 10 + random.randrange(1, thing['damage'])
                        print('It hits ' + mob['name'] + ' for ' + str(damage) + ' damage.')
                        mob['current_hp'] = mob['current_hp'] - damage
                        if mob['current_hp'] <= 0:
                            print('That was a fatal blow.')
                            mob['is_dead'] = True

                    else:
                        miss = random.randrange(1, 10)
                        if miss < 6:
                            print('It misses ' + mob['name'] + '.')
                        elif miss < 9:
                            print(mob['name'] + ' dodges the attack.')
                        else:
                            print('The attack glances off ' + mob['name'] + '.')

                    print(mob['name'] + ' ' + creature_wellness(mob['current_hp'], mob['max_hp']))
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
                if (mob['is_fatigued'] == False and mob['attack_chance'] >= random.randrange(1, 100)):
                    print(mob['name'] + ' attacks!')
                    mob['is_fatigued'] = True
                    if (random.randrange(1, 100) + mob['hit_bonus']) > 50:
                        damage = 10 + random.randrange(1, mob['damage'])
                        print('It hits you for ' + str(damage) + ' damage.')
                        player_hp = player_hp - damage
                        if player_hp <= 0:
                            print('That was a fatal blow.')
                    else:
                        miss = random.randrange(1, 10)
                        if miss < 6:
                            print('It misses you.')
                        elif miss < 9:
                            print('You dodge the attack.')
                        else:
                            print('The attack glances off you.')
                else:
                    hostile_posture = random.randrange(1, 3)
                    if hostile_posture == 1:
                        print(mob['name'] + ' gives you a hateful stare.')
                    elif hostile_posture == 2:
                        print(mob['name'] + ' catches its breath.')
                    else:
                        print(mob['name'] + ' readies for combat.')

                player_wellness(player_hp, 100)


def creature_follow(current_room, new_room):
    global room_has_mobs
    global player_hp
    global exit_room

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
    percentage = current / max * 100
    if percentage > 75:
        print("You are in good shape.")
    elif percentage > 50:
        print("You are in pain.")
    elif percentage > 25:
        print("You are hurting but still able to fight.")
    elif percentage > 0:
        print("You are seriously wounded.")
    else:
        print("You are dead.")


def weapon_checker(item):
    global inventory_quantity
    for thing in things:
        if thing['name'].lower() == item:
            if thing['is_weapon'] == True:
                return True
            else:
                return False


def pick_up_if_weapon(item):
    global inventory_quantity
    for thing in things:
        if thing['name'].lower() == item and thing['is_weapon'] == True:
            if thing['on_person'] == True:
                return
            thing['on_person'] = True
            inventory_quantity = inventory_quantity + 1
            print('You pick up the ' + thing['name'] + '.')


def available_targets(current_room):
    global inventory_quantity
    global room_has_items
    global target
    update_things_in_room(current_room)
    if room_has_items or inventory_quantity > 0:
        available_choices = []
        if room_has_items:
            for thing in things:
                if (thing['location'] == current_room and thing['on_person'] == False):
                    available_choices.append(thing['name'].lower())
        if inventory_quantity > 0:
            for thing in things:
                if (thing['on_person'] == True):
                    available_choices.append(thing['name'].lower())
    return available_choices


def check_event(current_room, used_item):
    # print('DEBUG: checking what happens when using ' + used_item + ' in room # ' + str(current_room))
    # print(events)
    for event in events:
        if (event['room'] == current_room and event['item_name'].lower() == used_item):
            if event['done'] == False:
                do_event(event['id'], current_room)
                return
            else:
                print(event['already_done_text'])
                return
        # problem if item can be used in 999 and in specific room - solution? make event index of specific room event lower than event index of any room 999? or have specific room inserted before 999?
        if (event['room'] == 999 and event['item_name'].lower() == used_item):
            if event['done'] == False:
                do_event(event['id'], current_room)
                return
            else:
                print(event['already_done_text'])
                return
    print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')


def do_event(event_id, current_room):
    global inventory_quantity
    global game_choice
    global player_hp

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
                           'location': 7, 'on_person': True, 'moveable': True, 'is_weapon': False})
            inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
            things.append({'name': 'egg shell', 'prefix': 'an',
                           'description': 'There\'s little to do with the broken egg shell shards.', 'location': 7,
                           'on_person': False, 'moveable': True, 'is_weapon': False})
            delete_thing('egg')
        # reveal basement
        if event_id in [5]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'toy house', 'prefix': 'a',
                           'description': 'This miniature colonial appears to be worn from play. You can imagine dolls going in and out of the doors and windows.',
                           'location': 6, 'on_person': False, 'moveable': True, 'is_weapon': False})
        # make birdhouse
        if event_id in [6]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'birdhouse', 'prefix': 'a',
                           'description': 'The toy house resting atop the post will surely attract small, avian creatures.',
                           'location': 1, 'on_person': False, 'moveable': False, 'is_weapon': False})
            delete_thing('toy house')
        # make flashlight
        if event_id in [11]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'flashlight', 'prefix': 'a',
                           'description': 'It\'s your standard issue flashlight. Looks like it could help you see in dark places, but it wouldn\'t do much elsewhere.',
                           'location': 9, 'on_person': False, 'moveable': True, 'is_weapon': False})
            delete_thing('coin')
        # make functional well
        if event_id in [17]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'well', 'prefix': 'the',
                           'description': 'The well is still old, but now you can raise and lower the bucket.',
                           'location': 10, 'on_person': False, 'moveable': False, 'is_weapon': False})
            delete_thing('broken well')
            delete_thing('bucket')
        # make key
        if event_id in [18]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({'name': 'key', 'prefix': 'a',
                           'description': 'The brass key is partially covered in moss. It feels heavy.', 'location': 10,
                           'on_person': False, 'moveable': True, 'is_weapon': False})
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
                           'on_person': True, 'moveable': True, 'is_weapon': False})
            inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
            delete_thing('elixir')
    elif game_choice == '3':
        # simple event: print text only, put weapons in here
        if event_id in [0]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
        if event_id in [1]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            player_hp = player_hp + 20
            if player_hp > 100:
                player_hp = 100
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
        # detention key card drops from guard upon death
        if event_id in [3]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM OR USE current_room VARIABLE
            things.append({'name': 'keycard', 'prefix': 'a',
                           'description': 'This sleek card reads, "Detention Elevator." Emblazoned under the text is an image of a box with an arrow inside it.',
                           'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False})



def delete_thing(thing_name):
    global inventory_quantity
    for thing in things:
        if thing['name'] == thing_name:
            if thing['on_person'] == True:
                inventory_quantity = inventory_quantity - 1
            things.remove(thing)


def show_exits(current_room):
    print('Visible exits:')
    for direction, destination in world[current_room]['exits'].items():
        if world[destination]['visible'] == True:
            print(full_direction(direction) + world[destination]['name'])


def get_move():
    global target
    global choice
    print('What do you want to do?')
    choice = input()
    target = extract_target(choice)
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
        return (command[(space_index + 1):])


def valid_move(from_key, direction):
    if direction in world[from_key]['exits'].keys():
        return True
    else:
        return False


def short_move(direction):
    if len(direction) == 9:
        return direction[0] + direction[5]
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
    print('COMMANDS'.center(72, '='))
    print('Here\'s a list of commands. They are not case sensitive.')
    print('To move around, you can type:')
    print('\'N\' or \'North\' to go north')
    print('\'NE\' or \'Northeast\' to go northeast')
    print('\'NW\' or \'Northwest\' to go northwest')
    print('\'S\' or \'South\' to go south')
    print('\'SE\' or \'Southeast\' to go southeast')
    print('\'SW\' or \'Southwest\' to go southwest')
    print('\'E\' or \'East\' to go east')
    print('\'W\' or \'West\' to go west')
    print('\'U\' or \'Up\' to go up')
    print('\'D\' or \'Down\' to go down')
    print('')
    print('To do things with items, you can type:')
    print('\'Use\' to use an item')
    print('\'X\' or \'Examine\' to inspect an item')
    print('\'Take\' to pick up an item and put it in your inventory')
    print('\'Drop\' to get rid of an item')
    print('You can type the action (use, examine, take, or drop) and the item, or just the action.')
    print('For example: If you want to use the apple, you can type \'use apple\' or \'use.\'')
    print('If you just type \'use,\' you will be asked what item you want to use.')
    print('')
    print('A note about combat: If you use a weapon on a creature, it will become hostile.')
    print('Hostile creatures will attack and follow you until stopped.')
    print('Using a weapon near a hostile creature will attack it.')
    print('')
    print('Other commands include:')
    print('\'L\' or \'Look\' to look around')
    print('\'I\' or \'Inv\' or \'Inventory\' to see what you are carrying')
    print('\'H\' or \'Health\' to check how you\'re feeling')
    print('\'?\' or \'Help\' to see this list of commands')
    print('\'Quit\' to quit the game')
    print('COMMANDS'.center(72, '='))


def show_intro():
    print(intro_text)
    print('')
    input('Press ENTER to continue...')
    show_help()
    print('')
    print('Good luck and have fun!')
    print('')


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
    global player_hp
    global starting_room
    global exit_room
    global intro_text
    global outro_text
    clear_game_vars()
    if choice == '1':
        world.insert(0, {'visible': True, 'name': 'House', 'prefix': 'in the',
                         'desc': 'This modest dwelling has one room on the ground floor. You can see the front yard to the east and the garage through a door to the south. One set of stairs leads up to the studio, and another goes down to the basement.',
                         'exits': {'e': 1, 's': 2, 'u': 8, 'd': 6}})
        world.insert(1, {'visible': True, 'name': 'Yard', 'prefix': 'in the',
                         'desc': 'The grass in the front yard is browning, and the flowers look sad. You can go west to back into the house, or go south around the house to the garage. Outside of the yard to the east is a street.',
                         'exits': {'w': 0, 's': 2, 'e': 3}})
        world.insert(2, {'visible': True, 'name': 'Garage', 'prefix': 'in the',
                         'desc': 'There is a musty smell, and oil stains cover the concrete floor. You can get to the house through the door to the north. The door to the yard is somehow stuck, but the main garage door to the east opens to the street.',
                         'exits': {'n': 0, 'e': 3}})
        world.insert(3, {'visible': True, 'name': 'Street', 'prefix': 'on the',
                         'desc': 'You don\'t see any cars on this strikingly ordinary street. The house is nearby. To the north is the gate to the front yard, and the garage door is open to the west. You see a dusty junkyard to the east. Following the road south will bring you to a park.',
                         'exits': {'n': 1, 'w': 2, 'e': 9, 's': 4}})
        world.insert(4, {'visible': True, 'name': 'Park', 'prefix': 'at the',
                         'desc': 'The wide, grassy clearing at the end of the road is accented by a few tall trees. Part of the grass is bare along the southern edge, and it contains a strange etching of a house and a winged creature. The street is at the north end of the park, a trail leads through the trees to the west, and a small meadow is to the east.',
                         'exits': {'n': 3, 'e': 10, 'w': 11}})
        world.insert(5, {'visible': False, 'name': 'Glowy portal', 'prefix': 'through the', 'desc': 'End description',
                         'exits': {}})
        world.insert(6, {'visible': True, 'name': 'Basement', 'prefix': 'in the',
                         'desc': 'It is really dark down here. And damp. Stairs lead back up into the house.',
                         'exits': {'u': 0}})
        world.insert(7, {'visible': False, 'name': 'Tree', 'prefix': 'up a',
                         'desc': 'You climb to the upper branches of the newly sprouted tree.', 'exits': {'d': 4}})
        world.insert(8, {'visible': True, 'name': 'Studio', 'prefix': 'in the',
                         'desc': 'An old painting hangs on the wall of this small space. Another wall has a large print of abstract shapes inside a circle. If you squint, you think the shapes represent something flying out of a tall structure, or they could be a square lollipop barfing feathers. A stairway goes back down to the main room.',
                         'exits': {'d': 0}})
        world.insert(9, {'visible': True, 'name': 'Junkyard', 'prefix': 'in the',
                         'desc': 'The air is thick in this run-down yard. Rusty scrap metal and mismatched tires are strewn about. The exit, back to the street, is on the west end of the junkyard.',
                         'exits': {'w': 3}})
        world.insert(10, {'visible': True, 'name': 'Meadow', 'prefix': 'in the',
                          'desc': 'This grassy spot is pleasant and wide. A lonely stone well sits in the middle. The park is to the west.',
                          'exits': {'w': 4}})
        world.insert(11, {'visible': True, 'name': 'Forest path', 'prefix': 'on the',
                          'desc': 'The dense woods are pierced by a well-worn trail. Looking west, the path appears to open into a dell. To the east, you see the park.',
                          'exits': {'e': 4, 'w': 12}})
        world.insert(12, {'visible': True, 'name': 'Dell', 'prefix': 'in the',
                          'desc': 'This gentle valley is surrounded by leafy trees and bushes. A path is visible to the east, and to the north you see a sturdy iron gate that fills the only opening in the foliage.',
                          'exits': {'e': 11}})
        world.insert(13, {'visible': False, 'name': 'Winding passageway', 'prefix': 'in a',
                          'desc': 'This jaunty tunnel is dimly lit by bioluminescent lichen. So pretty! The open iron gate is at the south end of the passage. As it bends to the northeast, it goes deeper and deeper into the earth.',
                          'exits': {'s': 12, 'ne': 14}})
        world.insert(14, {'visible': True, 'name': 'Subbasement', 'prefix': 'in the',
                          'desc': 'This tiny, chilly room opens west to a winding passageway. There\'s a trick one-way trapdoor in the ceiling, which you can access using handholds cut into the wall.',
                          'exits': {'sw': 13, 'u': 6}})

        starting_room = 0
        exit_room = 5
        player_hp = 100

        things.append({'name': 'note', 'prefix': 'a',
                       'description': 'Something is badly scrawled on this yellowing paper, but with effort, you can read it. \n\'If you don\'t like it here, exit through the portal.\nObviously, portals aren\'t naturally occuring.\nYou\'ll have to summon one.\nI think there\'s a clue in the studio.\'',
                       'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': False})
        things.append({'name': 'pebble', 'prefix': 'a',
                       'description': 'This tiny rock has been smoothed by eons of natural erosion. How could something so small be so old?',
                       'location': 1, 'on_person': False, 'moveable': True, 'is_weapon': False})
        things.append(
            {'name': 'ball', 'prefix': 'a', 'description': 'It\'s a dark pink playground ball.', 'location': 4,
             'on_person': False, 'moveable': True, 'is_weapon': False})
        things.append({'name': 'Mona Lisa', 'prefix': 'the',
                       'description': 'This painting is a masterpiece of the Italian Renaissance. There is something to that smile.',
                       'location': 8, 'on_person': False, 'moveable': False, 'is_weapon': False})
        things.append({'name': 'tricycle', 'prefix': 'a',
                       'description': 'The light blue aluminum tricycle appears to be in working order, though that plastic seat doesn\'t seem comfortable.',
                       'location': 3, 'on_person': False, 'moveable': True, 'is_weapon': False})
        things.append({'name': 'tree kit', 'prefix': 'a',
                       'description': 'The tree kit box claims: \'Makes a real life tree in seconds! No digging required. For best results, use in an open area.\'',
                       'location': 2, 'on_person': False, 'moveable': True, 'is_weapon': False})
        things.append({'name': 'egg', 'prefix': 'an',
                       'description': 'The small, blue egg feels weighty, like there\'s something inside it.',
                       'location': 7, 'on_person': False, 'moveable': True, 'is_weapon': False})
        things.append({'name': 'post', 'prefix': 'a',
                       'description': 'It\'s four feet tall, stuck in the ground, and has a little square table surface at the top.',
                       'location': 1, 'on_person': False, 'moveable': False, 'is_weapon': False})
        things.append({'name': 'machine', 'prefix': 'a',
                       'description': 'You try to make sense of this large, well-maintained, metallic box. It is the size of a refrigerator but without any visible doors. It has two holes: a small slot near the top and a large square hole at the bottom.',
                       'location': 9, 'on_person': False, 'moveable': False, 'is_weapon': False})
        things.append({'name': 'broken well', 'prefix': 'a',
                       'description': 'It looks like this old well isn\'t completely broken. The crank turns, adjusting the height of the rope, but nothing is attached to it. At the bottom of the well, something reflects light back up to you.',
                       'location': 10, 'on_person': False, 'moveable': False, 'is_weapon': False})
        things.append({'name': 'bucket', 'prefix': 'a',
                       'description': 'This yellow bucket has a wide handle at the top, making it easy to hold.',
                       'location': 2, 'on_person': False, 'moveable': True, 'is_weapon': False})
        things.append({'name': 'coin', 'prefix': 'a',
                       'description': 'This rusty coin has indecipherable symbols on one side and a rectangular shape on the other. It doesn\'t appear to be worth much.',
                       'location': 13, 'on_person': False, 'moveable': True, 'is_weapon': False})
        things.append({'name': 'gate', 'prefix': 'a',
                       'description': 'This is a serious gate. The wrought-iron frame is elegant yet ominous. You see a bulky, brass lock mechanism that contains a happy keyhole.',
                       'location': 12, 'on_person': False, 'moveable': False, 'is_weapon': False})

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
                           'first_time_text': 'Something is badly scrawled on this yellowing paper, but with effort, you can read it. \'If you don\'t like it here, exit through the portal. Obviously, portals aren\'t naturally occuring. You\'ll have to summon one. I think there\'s a clue in the studio.\'',
                           'already_done_text': 'Something is badly scrawled on this yellowing paper, but with effort, you can read it. \'If you don\'t like it here, exit through the portal. Obviously, portals aren\'t naturally occuring. You\'ll have to summon one. I think there\'s a clue in the studio.\''})
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

        intro_text = 'Well, this is odd. You find yourself in an unfamiliar house.\nYou don\'t remember how you got here. You just know this isn\'t real.\nLook around and use things. If the way forward is not clear, keep looking. And using.\n\nYou must escape and get back to reality!'
        outro_text = 'Congratulations! You escaped that odd world and are back in reality.'


    elif choice == '2':
        world.insert(0, {'visible': True, 'name': 'Start', 'prefix': 'at the',
                         'desc': 'This bare room is an octagon. You see a door in the southeast wall.',
                         'exits': {'se': 1}})
        world.insert(1, {'visible': True, 'name': 'End', 'prefix': 'at the',
                         'desc': 'Packed dirt covers the floor of this spacious arena. A door is in the northwest corner. On the south wall, the word "EXIT" is painted in what could be dried blood. Or maybe ketchup? Below it is a large pit. You could probably climb down into it.',
                         'exits': {'nw': 0, 'd': 2}})
        world.insert(2, {'visible': True, 'name': 'Exit', 'prefix': 'out the', 'desc': 'End description', 'exits': {}})
        starting_room = 0
        exit_room = 2
        player_hp = 100
        things.append({'name': 'hammer', 'prefix': 'a',
                       'description': 'It\'s a classic ball-peen hammer. Could do some real damage.', 'location': 0,
                       'on_person': False, 'moveable': True, 'is_weapon': True, 'damage': 35, 'hit_bonus': 20})
        things.append(
            {'name': 'cog', 'prefix': 'a', 'description': 'This rusty machine cog is worn down from years of use.',
             'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': False})
        things.append({'name': 'elixir', 'prefix': 'an',
                       'description': 'A small glass bottle contains a bright green liquid. The label reads: "Drink for fast-acting relief."',
                       'location': 1, 'on_person': False, 'moveable': True, 'is_weapon': False})
        events.insert(0, {'id': 0, 'done': False, 'room': 999, 'item_name': 'Hammer',
                          'first_time_text': 'You swing the hammer.', 'already_done_text': 'You swing the hammer.'})
        events.insert(1, {'id': 1, 'done': False, 'room': 1, 'item_name': 'elixir',
                          'first_time_text': 'You open the bottle and gulp down the contents. It tastes like ecto-cooler. Regardless, you feel a surge of wellness in your body.',
                          'already_done_text': 'The small bottle is empty. What a shame.'})
        creatures.append({'id': 0, 'name': 'Monster',
                          'description': 'The monster is about 7 feet tall, covered in yellow fur, and shows sharp teeth and claws.',
                          'room': 0, 'max_hp': 100, 'current_hp': 100, 'is_dead': False, 'is_hostile': False,
                          'status_neutral': 'It isn\'t interested in you.', 'status_hostile': 'It\'s very mad at you.',
                          'damage': 30, 'hit_bonus': 20, 'attack_chance': 75, 'is_fatigued': False, 'death_event': 0})
        intro_text = 'This is just a small world to get used to combat.\n\nWhen you get tired of fighting, just drop into the pit.'
        outro_text = 'Welp, you survived. The real challenge lies ahead.'

    elif choice == '3':
        starting_room = 0
        exit_room = 99
        player_hp = 100
        intro_text = 'This is the space adventure.\n\nEnjoy!'
        outro_text = 'You conquered the Space adventure.'

        world.insert(0, {'visible': True, 'name': 'Cell', 'prefix': 'in a',
                         'desc': 'This cell has a single door to the north.',
                         'exits': {'n': 1}})
        world.insert(1, {'visible': True, 'name': 'Detention hallway', 'prefix': 'in the',
                         'desc': 'This long hallway has an elevator bay to the west. The hallway continues to the east. There is an open cell to the south.',
                         'exits': {'w': 4, 'e': 2, 's': 0}})
        world.insert(2, {'visible': True, 'name': 'Back hallway', 'prefix': 'in the',
                         'desc': 'This is the end of the detention hallway. Back west is the main hallway. A small door is on the north wall.',
                         'exits': {'w': 1, 'n': 3}})
        world.insert(3, {'visible': True, 'name': 'Storage closet', 'prefix': 'in a',
                         'desc': 'The only exit from this closet is south.',
                         'exits': {'s': 2}})
        world.insert(4, {'visible': True, 'name': 'Detention Level Elevator Bay', 'prefix': 'at the',
                         'desc': 'The elevator goes up to the Main Deck, but it require a keycard to activate it. The detention hallway is to the east.',
                         'exits': {'e': 1}})
        world.insert( 5, {'visible': False, 'name': 'Main Deck Elevator Bay 5', 'prefix': 'at',
                          'desc': 'The elevator goes down to the Detention Level. To the west is a security checkpoint.',
                          'exits': {'w': 6, 'd': 4}})
        world.insert( 6, {'visible': True, 'name': 'Main Deck Security Desk', 'prefix': 'at a',
                          'desc': 'This is the Main Deck Security Checkpoint. To the east is an elevator bay to the Detention Level. To the south is an elevator bay to the Engine Room. A walkway is visible to the west.',
                          'exits': {'e': 5, 's': 7, 'w': 8}})
        world.insert( 7, {'visible': True, 'name': 'Main Deck Elevator Bay 4', 'prefix': 'at',
                          'desc': 'The elevator goes down to the Engine Room. To the north is a security checkpoint.',
                          'exits': {'n': 6, 'd': 14}})
        world.insert( 8, {'visible': True, 'name': 'Walkway', 'prefix': 'in the',
                          'desc': 'This walkway connects the Main Deck Security Desk to the East and a wide hallway to the West. North is an elevator bay to the Hangar.',
                          'exits': {'e': 6, 'n': 9, 'w': 10}})
        world.insert( 9, {'visible': True, 'name': 'Main Deck Elevator Bay 3', 'prefix': 'at',
                          'desc': 'The elevator goes down to the Hangar. To the south is a walkway.',
                          'exits': {'s': 8, 'd': 19}})
        world.insert( 10, {'visible': True, 'name': 'Wide hallway', 'prefix': 'in the',
                          'desc': 'This wide hallway branches in several directions. To the east is a walkway. South is an elevator to the Armory. To the west, the hallway continues toward the front of the ship.',
                          'exits': {'e': 8, 's': 11, 'w': 12}})
        world.insert( 11, {'visible': True, 'name': 'Main Deck Elevator Bay 2', 'prefix': 'at',
                          'desc': 'The elevator goes down to the Armory. To the north is a wide, branching hallway.',
                          'exits': {'d': 23, 'n': 10}})
        world.insert( 12, {'visible': True, 'name': 'Hallway', 'prefix': 'in the',
                          'desc': 'The hallway narrows as it leads from east to west. At the east end is a wide, branching hallway. To the west is an elevator to the Quarters.',
                          'exits': {'e': 10, 'w': 13}})
        world.insert( 13, {'visible': True, 'name': 'Main Deck Elevator Bay 1', 'prefix': 'at',
                          'desc': 'The elevator goes down to Crew Quarters. To the east is a widening hallway.', 'exits': {'d': 28, 'e': 12}})
        world.insert( 14, {'visible': True, 'name': 'Engine Room Elevator Bay', 'prefix': 'at the',
                          'desc': 'The elevator goes up to the Main Deck. To the east is the Engine Room.', 'exits': {'u': 7, 'e': 15}})
        world.insert( 15, {'visible': True, 'name': 'Engine Room', 'prefix': 'in the',
                          'desc': 'The loud, pusling motor fills up most of the room. To the north and south are fuel cell storage rooms. An equipment room is to the east. To the west is an elevator bay.',
                          'exits': {'n': 16, 'e': 17, 's': 18, 'w': 14}})
        world.insert( 16, {'visible': True, 'name': 'North fuel cell storage', 'prefix': 'in the',
                           'desc': 'This room is filled with unused fuel cells. The only exit is to the south.',
                          'exits': {'s': 15}})
        world.insert( 17, {'visible': True, 'name': 'Engine Equipment Room', 'prefix': 'in the',
                           'desc': 'Spare parts, tools, and complex monitoring consoles fill this room. To the west is the engine room.',
                          'exits': {'w': 15}})
        world.insert( 18, {'visible': True, 'name': 'South fuel cell storage', 'prefix': 'in the',
                           'desc': 'This room is filled with empty fuel cells. The only exit is to the north.',
                           'exits': {'n': 15}})
        world.insert( 19, {'visible': True, 'name': 'Hangar Elevator Bay', 'prefix': 'at the',
                           'desc': 'The elevator goes up to the Main Deck. To the east is a wide entrance to the Hangar.',
                           'exits': {'u': 9, 'e': 20}})
        world.insert( 20, {'visible': True, 'name': 'Hangar', 'prefix': 'in the',
                           'desc': 'This large room contains supply crates and a small, disassembled starship. Escape pods are in the southeast and southwest corners of the room. To the west is the elevator bay.',
                           'exits': {'w': 19, 'se': 21, 'sw': 22}})
        world.insert( 21, {'visible': True, 'name': 'Escape pod B14', 'prefix': 'in', 'desc': 'This small pod is surprisingly comfortable. The exit to the Hangar is to the northwest.',
                           'exits': {'nw': 20}})
        world.insert( 22, {'visible': True, 'name': 'Escape pod L07', 'prefix': 'in', 'desc': 'This small pod is cozy. The exit to the Hangar is to the northeast.',
                           'exits': {'ne': 20}})
        world.insert( 23, {'visible': True, 'name': 'Armory Elevator Bay', 'prefix': 'at the',
                           'desc': 'This elevator goes up to the Main Deck. To the south is a security checkpoint.', 'exits': {'u': 11, 's': 24}})
        world.insert( 24, {'visible': True, 'name': 'Armory Security Desk', 'prefix': 'at the',
                           'desc': 'This is the heavily-fortified Armory Security Desk. To the east is the Guard Auxilary. To the north is an elevator bay.',
                           'exits': {'n': 23, 'e': 25}})
        world.insert( 25, {'visible': True, 'name': 'Guard Auxilary', 'prefix': 'in the',
                           'desc': 'The scent of battle is inescapable. Two storage rooms are accessible: Weapons to the north and Supplies to the east. The security checkpoint is to the west.',
                           'exits': {'w': 24, 'n': 26, 'e': 27}})
        world.insert( 26, {'visible': True, 'name': 'Weapons storage room', 'prefix': 'in the',
                           'desc': 'Implements of destruction fill every corner of this room. Most of them are beyond understanding. The only exit is south.',
                           'exits': {'s': 25}})
        world.insert( 27, {'visible': True, 'name': 'Armory supply room', 'prefix': 'in the',
                           'desc': 'This room contains many strange devices. The exit is to the west.',
                           'exits': {'w': 25}})
        world.insert( 28, {'visible': True, 'name': 'Quarters Elevator Bay 3', 'prefix': 'at',
                           'desc': 'This elevator goes up to the Main Deck. To the north is the lounge.',
                           'exits': {'n': 29, 'u': 13}})
        world.insert( 29, {'visible': True, 'name': 'Lounge', 'prefix': 'in the',
                           'desc': 'The lounge is perfect for resting and recreation. Tables, comfy chairs, and several entertainment consoles are thoughtfully arranged. A wide observation deck is visible to the west. To the east is the dormitory. An elevator to the Main Deck is at the south end of the room.',
                           'exits': {'s': 28, 'w': 32, 'e': 30}})
        world.insert( 30, {'visible': True, 'name': 'Dormitory', 'prefix': 'in the',
                           'desc': 'Rows and rows of empty sleeping pods fill the room. To the east are what look like grooming facilities. The lounge is accessible to the west.',
                           'exits': {'w': 29, 'e': 31}})
        world.insert( 31, {'visible': True, 'name': 'Crew Facilities', 'prefix': 'in the',
                           'desc': 'Toilets, showers, and hygiene facilities are arranged to maximize privacy. The dormitory is to the west.',
                           'exits': {'w': 30}})
        world.insert( 32, {'visible': True, 'name': 'Observation Deck', 'prefix': 'in the',
                           'desc': 'A floor-to-ceiling view to the west shows all that is visible in front of this spacecraft. Tables and seating is positioned to provide a relaxing view. Elevator bays are on each side of the large window. An elevator to the bridge is to the north, and an elevator to the mess hall is to the south. To the east is the lounge area.',
                           'exits': {'n': 33, 'e': 29, 's': 34}})
        world.insert( 33, {'visible': True, 'name': 'Quarters Elevator Bay 1', 'prefix': 'at',
                           'desc': 'This elevator goes up to the Bridge. To the south is the observation deck.',
                           'exits': {'u': 42, 's': 32}})
        world.insert( 34, {'visible': True, 'name': 'Quarters Elevator Bay 2', 'prefix': 'at',
                           'desc': 'This elevator goes down to the Mess Hall and Support Services. The observation deck is to the north.',
                           'exits': {'d': 35, 'n': 32}})
        world.insert( 35, {'visible': True, 'name': 'Mess Elevator Bay', 'prefix': 'at the',
                           'desc': 'This elevator goes up to the Quarters. To the east is the mess hall. South is a room called Support Services A.',
                           'exits': {'e': 38, 's': 36, 'u': 34}})
        world.insert( 36, {'visible': True, 'name': 'Support Services A', 'prefix': 'in',
                           'desc': 'There is a small waiting area and a desk. To the north is an elevator bay. East is a room labeled Support Services B.',
                           'exits': {'n': 35, 'e': 37}})
        world.insert( 37, {'visible': True, 'name': 'Support Services B', 'prefix': 'in',
                           'desc': 'Several cubbies with desks and chairs are situated in each corner. The east wall is filled with cabinets and drawers. The only exit is to the west.',
                           'exits': {'w': 36}})
        world.insert( 38, {'visible': True, 'name': 'Mess Hall', 'prefix': 'in the',
                           'desc': 'This large room has neat rows of tables and a service area. The kitchen entrance is next to the service area on the north wall. Large double-doors connect a storage closet to the east. An elevator bay is to the west.',
                           'exits': {'n': 39, 'e': 41, 'w': 35}})
        world.insert( 39, {'visible': True, 'name': 'Kitchen', 'prefix': 'in the',
                           'desc': 'All kinds of food preparation and preservation devices are visible. A service area and doorway to the mess hall is to the south. The east wall connects to a deep walk-in pantry.',
                           'exits': {'s': 38, 'e': 40}})
        world.insert( 40, {'visible': True, 'name': 'Pantry', 'prefix': 'in the',
                           'desc': 'Dry and packaged foods in boxes, bins, and bags line the shelves. A cold-storage unit is built into the north wall. To the west is the kitchen.',
                           'exits': {'w': 39}})
        world.insert( 41, {'visible': True, 'name': 'Storage and cleaning closet', 'prefix': 'in the',
                           'desc': 'This well-stocked closet holds dining implements, cleaning solutions, and scrubbing mechanisms. The mess hall is to the west.',
                           'exits': {'w': 38}})
        world.insert( 42, {'visible': True, 'name': 'Bridge Elevator Bay', 'prefix': 'at the',
                           'desc': 'This elevator goes down to the Quarters. To the north is a security checkpoint.',
                           'exits': {'d': 33, 'n': 43}})
        world.insert( 43, {'visible': True, 'name': 'Bridge Security Desk', 'prefix': 'at the',
                           'desc': 'This is the bridge-level security desk. A door to the bridge is to the west. To the east is the Systems Control room. South is an elevator bay.',
                           'exits': {'w': 44, 'e': 45, 's': 42}})
        world.insert( 44, {'visible': True, 'name': 'Bridge', 'prefix': 'on the',
                           'desc': 'Even though it is called a bridge, it is more like a glorified cockpit. Flight controls and communications consoles are positioned near the officer chairs. East is the security desk.',
                           'exits': {'e': 43}})
        world.insert( 45, {'visible': True, 'name': 'Systems Control room', 'prefix': 'in the',
                           'desc': 'Data from the ship\'s environment control, propulsion, and weapons systems are a few of things displayed on huge screens in this room. The only way out is west to the security desk.',
                           'exits': {'w': 43}})

        things.append({'name': 'Food tray', 'prefix': 'a', 'description': 'The empty food tray has some heft to it. The metal edge looks mean.',
                       'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': True, 'damage': 10, 'hit_bonus': 25})
        things.append({'name': 'Stimpack', 'prefix': 'a', 'description': 'A small vial of clear liquid has a red heart decal on the side.',
                       'location': 3, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0})



        events.insert(0, {'id': 0, 'done': False, 'room': 999, 'item_name': 'Food tray',
                          'first_time_text': 'You swing the food tray.', 'already_done_text': 'You swing the food tray.'})
        events.insert(1, {'id': 1, 'done': False, 'room': 999, 'item_name': 'stimpack',
                          'first_time_text': 'You jab the stimpack into your thigh. Heat rushes through your body, and you feel much better.',
                          'already_done_text': 'The stimpack is used up.'})
        # note 3 before 2 because 999 event needs to come AFTER room-specific event
        events.insert(3, {'id': 3, 'done': False, 'room': 999, 'item_name': 'Keycard',
                          'first_time_text': 'As the guard falls to the floor, a keycard falls from his pocket.', 'already_done_text': 'Judging by its markings, this seems like it would be useful at the Detention Elevator Bay.'})
        events.insert(2, {'id': 2, 'done': False, 'room': 4, 'item_name': 'Keycard',
                          'first_time_text': 'The keycard fits nicely into the elevator console. You can now use the elevator!', 'already_done_text': 'This elevator is already accessible.'})

        creatures.append({'id': 0, 'name': 'Prison guard',
                          'description': 'The guard is 6 feet tall with a sturdy build, greenish skin, and eyes that are cloudy and dark. Its posture is full of anger. No weapons are visible, but its knuckles look pointy.',
                          'room': 1, 'max_hp': 40, 'current_hp': 40, 'is_dead': False, 'is_hostile': True,
                          'status_neutral': 'It isn\'t interested in you.', 'status_hostile': 'It\'s very mad at you.',
                          'damage': 10, 'hit_bonus': 10, 'attack_chance': 65, 'is_fatigued': False, 'death_event': 3})




def initialize_engine():
    global allowed_moves
    global allowed_actions
    global inventory_quantity
    global room_has_items
    global room_has_mobs
    global locale_visited
    global available_games
    allowed_moves = ['n', 'north', 's', 'south', 'e', 'east', 'w', 'west', 'u', 'up', 'd', 'down', 'ne', 'northeast',
                     'nw', 'northwest', 'se', 'southeast', 'sw', 'southwest']
    allowed_actions = ['l', 'look', 'x', 'examine', 'use', 'take', 'drop', 'i', 'inv', 'inventory', '?', 'help', 'quit', 'h',
                       'health']
    inventory_quantity = 0
    room_has_items = False
    room_has_mobs = False
    locale_visited = False
    available_games = ['1', '2', '3']


def select_game():
    global available_games
    print('Choose a text game by number:')
    print('1 - OG Portal')
    print('2 - Combat practice')
    print('3 - Space adventure')
    print('Your choice?')
    game_choice = input()
    while game_choice not in available_games:
        print('Enter a number from the above list to choose a text game.')
        game_choice = input()
    return game_choice


# main code starts here
initialize_engine()
print('Welcome to Text Games!')
print('')
game_choice = select_game()
load_game(game_choice)
print('')

room = starting_room
show_intro()
while room != exit_room:
    remove_creature_fatigue(room)
    if player_hp <= 0:
        print('Thanks for playing!')
        print('')
        input('Press ENTER to continue...')
        break
    if locale_visited == False:
        locale(room)
        locale_visited = True
    move = get_move()
    if move == '?' or move == 'help':
        show_help()
    elif move == 'l' or move == 'look':
        look_around(room)
    elif move == 'x' or move == 'examine':
        examine_item(room)
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
            input('Press ENTER to continue...')
            break
        else:
            print('Okay, back to it.')
    else:
        dir = short_move(move)
        if valid_move(room, dir) == True:
            new_room = world[room]['exits'][dir]
            creature_follow(room, new_room)
            room = new_room
            locale_visited = False
        else:
            print('You can\'t go that way.')
    print('')

if room == exit_room:
    print(outro_text)
    print('')
    input('Press ENTER to continue...')
