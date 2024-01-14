#! python3
# TextGames
# version 1.4.5
# description: splitting game files

# imports
import random

# function added for conversion to windows .exe
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# functions
def locale(current_room):
    print('You are ' + world[current_room]['prefix'] + ' ' + world[current_room]['name'] + world[current_room]['name2'] + '.')
    print(world[current_room]['desc'])
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
                if (thing['on_person'] == True):
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
        return "is in good shape." + " (" + str(current) + "\\" + str(max) + ")"
    elif percentage > 50:
        return "appears to be in some pain." + " (" + str(current) + "\\" + str(max) + ")"
    elif percentage > 25:
        return "is hurting but still dangerous." + " (" + str(current) + "\\" + str(max) + ")"
    elif percentage > 0:
        return "is seriously wounded." + " (" + str(current) + "\\" + str(max) + ")"
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
        print('You don\'t see anything special.')
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
            if (thing['location'] == current_room and thing['on_person'] == False):
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
            if (thing['on_person'] == True):
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
                pick_up_if_weapon(target)
                if attack_checker(current_room):
                    check_event(current_room, target)
                    player_attack(current_room, target)
                else:
                    check_event(current_room, target)
            else:
                check_event(current_room, target)
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
                if (thing['location'] == current_room and thing['on_person'] == False):
                    print(thing['name'].capitalize())
                    available_choices.append(thing['name'].lower())
        if inventory_quantity > 0:
            for thing in things:
                if (thing['on_person'] == True):
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
            pick_up_if_weapon(choice)
            if attack_checker(current_room):
                check_event(current_room, choice)
                player_attack(current_room, choice)
            else:
                check_event(current_room, choice)
        else:
            check_event(current_room, choice)
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

                    if (random.randrange(1, 100) + thing['hit_bonus']) > 50:
                        damage = thing['base_damage'] + random.randrange(1, thing['damage'])
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
    global move
    global last_move

    percentage = current / max * 100
    if percentage > 75:
        print("You are in good shape. (" + str(current) + "\\" + str(max) + ')')
    elif percentage > 50:
        print("You are in some pain. (" + str(current) + "\\" + str(max) + ')')
    elif percentage > 25:
        print("You are hurting but still able to fight. (" + str(current) + "\\" + str(max) + ')')
    elif percentage > 0:
        print("You are seriously wounded. (" + str(current) + "\\" + str(max) + ')')
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
    if room_has_items or inventory_quantity > 0:
        available_choices = []
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
    print('\t\'?\' or \'Help\' to see this list of commands')
    print('\t\'Quit\' to quit the game')
    print('COMMANDS'.center(72, '='))
    last_move = move


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

    clear_game_vars()

    if choice == '1':
        from game_1 import world, things, creatures, events, player_hp, starting_room, exit_room, intro_text, outro_text
        from game_1 import do_event, do_special
    elif choice == '2':
        from game_2 import world, things, creatures, events, player_hp, starting_room, exit_room, intro_text, outro_text
        from game_2 import do_event, do_special
    elif choice == '3':
        from game_3 import world, things, creatures, events, player_hp, starting_room, exit_room, intro_text, outro_text, special_rooms, special_done, launch_code
        from game_3 import do_event, do_special

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
    allowed_moves = ['n', 'north', 's', 'south', 'e', 'east', 'w', 'west', 'u', 'up', 'd', 'down', 'ne', 'northeast',
                     'nw', 'northwest', 'se', 'southeast', 'sw', 'southwest']
    allowed_actions = ['l', 'look', 'x', 'examine', 'use', 'take', 'drop', 'i', 'inv', 'inventory', '?', 'help', 'quit', 'h',
                       'health', 'r', 'repeat']
    inventory_quantity = 0
    room_has_items = False
    room_has_mobs = False
    locale_visited = False
    available_games = ['1', '2', '3']
    special_rooms = []
    special_done = []

def select_game():
    global available_games
    print('Choose a text game by number:')
    print('1 - OG Portal')
    print('2 - Combat practice')
    print('3 - Space adventure')
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
    if move == "" or move == '' or move == None:
        pass
    elif move == '?' or move == 'help':
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
