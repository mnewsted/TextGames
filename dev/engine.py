"""
Core game engine: room display, item interaction, movement, and input parsing.

Imports combat functions (including wellness helpers) but not save_load —
the game loop in main.py wires those together.

update_things_in_room() is gone; room_has_items / room_has_mobs are now
computed @property methods on GameState.
delete_thing() is gone from here; it lives on GameState as state.delete_thing().
load_game / clear_game_vars are gone; state.load_world() replaces them.
"""

import random

from events import check_event, do_special
from combat import (
    attack_checker, pick_up_if_weapon, player_attack,
    creature_attack, creature_attack_block,
    creature_wellness, player_wellness,
    weapon_checker, defense_checker,
)

# ---------------------------------------------------------------------------
# Constants (replaces initialize_engine globals)
# ---------------------------------------------------------------------------

ALLOWED_MOVES = [
    'n', 'north', 's', 'south', 'e', 'east', 'w', 'west',
    'u', 'up', 'd', 'down',
    'ne', 'northeast', 'nw', 'northwest',
    'se', 'southeast', 'sw', 'southwest',
]

ALLOWED_ACTIONS = [
    'l', 'look', 'x', 'examine', 'use', 'take', 'drop',
    'i', 'inv', 'inventory',
    '?', 'help', 'quit',
    'h', 'health',
    'r', 'repeat',
    'v', 'verbose',
    'save', 'load',
]

AVAILABLE_GAMES = ['1', '2', '3', '4']


# ---------------------------------------------------------------------------
# Room display
# ---------------------------------------------------------------------------

def locale(current_room, state, world_module):
    """Print room description, items, creatures, and fire specials."""
    # World 4 room 12: transform BEFORE showing the room description
    if state.game_choice == '4' and current_room == 12:
        if current_room in state.special_rooms:
            do_special(current_room, state, world_module)

    room = state.world[current_room]
    print(f'You are {room["prefix"]} {room["name"]}{room["name2"]}.')
    print(room['desc'])

    if state.verbose_mode and not state.locale_visited:
        show_exits(current_room, state)

    show_things(current_room, state)
    show_creatures(current_room, state)

    if current_room in state.special_rooms:
        do_special(current_room, state, world_module)


def look_around(current_room, state):
    room = state.world[current_room]
    print(f'You are {room["prefix"]} {room["name"]}{room["name2"]}.')
    print(room['desc'])
    show_exits(current_room, state)
    show_things(current_room, state)
    show_creatures(current_room, state)
    state.last_move = state.move


def show_exits(current_room, state):
    print('Visible exits:')
    for direction, dest in state.world[current_room]['exits'].items():
        if state.world[dest]['visible']:
            print(full_direction(direction) + state.world[dest]['name'])


def show_things(current_room, state):
    items = [t for t in state.things if t['location'] == current_room and not t['on_person']]
    if items:
        print('Visible items:')
        for thing in items:
            print(thing['prefix'].capitalize() + ' ' + thing['name'])


def show_creatures(current_room, state):
    for mob in state.creatures:
        if mob['room'] != current_room:
            continue
        if not mob['is_dead']:
            status = mob['status_hostile'] if mob['is_hostile'] else mob['status_neutral']
            print(mob['name'] + ' is here. ' + status)
            if not mob['was_seen']:
                print(mob['description'] + '\n')
                mob['was_seen'] = True
        else:
            print(mob['name'] + " is here, but it's dead.")


def show_inventory(state):
    if state.inventory_quantity > 0:
        print('You are carrying:')
        for thing in state.things:
            if thing['on_person']:
                print(thing['prefix'].capitalize() + ' ' + thing['name'])
    else:
        print("You aren't carrying anything.")
    state.last_move = state.move


def show_intro(state):
    show_short_help()
    print('')
    print(state.intro_text)


def show_short_help():
    print("Enter '?' or 'Help' to see a list of commands.")


def show_help(state):
    print('COMMANDS'.center(72, '='))
    print("Here's a list of commands. They ARE NOT case sensitive.")
    print('To move around, you can type:')
    print("\t'N' or 'North' to go north")
    print("\t'NE' or 'Northeast' to go northeast")
    print("\t'NW' or 'Northwest' to go northwest")
    print("\t'S' or 'South' to go south")
    print("\t'SE' or 'Southeast' to go southeast")
    print("\t'SW' or 'Southwest' to go southwest")
    print("\t'E' or 'East' to go east")
    print("\t'W' or 'West' to go west")
    print("\t'U' or 'Up' to go up")
    print("\t'D' or 'Down' to go down")
    print('')
    print('To do things with items, you can type:')
    print("\t'Use' to use an item")
    print("\t'X' or 'Examine' to inspect an item")
    print("\t'Take' to pick up an item and put it in your inventory")
    print("\t'Drop' to get rid of an item")
    print("You can type the action (use, examine, take, or drop) and the item name, or just the action.")
    print("For example: If you want to use the apple, you can type 'use apple' or 'use.'")
    print("If you just type 'use,' you will be asked what item you want to use.")
    print('')
    print('A few notes about creatures and combat:')
    print('Creatures can be friendly or hostile (mean).')
    print('If you use a weapon near a friendly creature, you will be asked if you want to attack it.')
    print('Attacking a friendly creature will make it hostile, obviously.')
    print('Using a weapon near a hostile creature will always attack it.')
    print('Hostile creatures will attack and follow you until stopped.')
    print('')
    print('Other commands include:')
    print("\t'L' or 'Look' to look around")
    print("\t'I' or 'Inv' or 'Inventory' to see what you are carrying")
    print("\t'H' or 'Health' to check how you're feeling")
    print("\t'R' or 'Repeat' to repeat the last valid command (without re-typing the whole thing!)")
    print("\t'V' or 'Verbose' to turn OFF and ON the automatic display of visible exits")
    print("\t'Save' to save your progress")
    print("\t'Load' to load your progress from a game you saved earlier")
    print("\t'?' or 'Help' to see this list of commands")
    print("\t'Quit' to quit the game")
    print('COMMANDS'.center(72, '='))
    state.last_move = state.move


def toggle_verbose(state):
    if state.verbose_mode:
        state.verbose_mode = False
        print("Verbose mode is turned OFF. Use the 'Look' command to see a list of visible exits.")
        print("If you want to switch back to Verbose mode, type 'V' or 'Verbose'.")
    else:
        state.verbose_mode = True
        print('Verbose mode is turned ON. Visible exits will automatically display when entering a location.')
        print("If you want to turn OFF Verbose mode, type 'V' or 'Verbose'.")


# ---------------------------------------------------------------------------
# Item interaction
# ---------------------------------------------------------------------------

def available_targets(current_room, state):
    """Return a list of item names the player can interact with (room + inventory)."""
    choices = []
    for thing in state.things:
        if thing['location'] == current_room and not thing['on_person']:
            choices.append(thing['name'].lower())
    for thing in state.things:
        if thing['on_person']:
            choices.append(thing['name'].lower())
    return choices


def examine_item(current_room, state):
    target = state.target

    # Direct target provided and it names a known item
    if target:
        for thing in state.things:
            if thing['name'].lower() == target.lower():
                if thing['location'] == current_room or thing['on_person']:
                    print(thing['description'])
                    state.last_move = state.move + ' ' + target
                    return

        # Check if target names a creature in this room (dead or alive)
        for mob in state.creatures:
            if mob['room'] == current_room and mob['name'].lower() == target.lower():
                if mob['is_dead']:
                    print(mob['dead_description'])
                else:
                    print(mob['description'] + '\n' + mob['name'] + ' '
                          + creature_wellness(mob['current_hp'], mob['max_hp']), end='')
                    if mob['is_hostile']:
                        print(' ' + mob['status_hostile'])
                    else:
                        print(' ' + mob['status_neutral'])
                state.last_move = state.move
                return

    # No valid target specified — show menu
    has_anything = (state.room_has_items or state.inventory_quantity > 0
                    or any(m['room'] == current_room for m in state.creatures))
    if not has_anything:
        print("There isn't anything to examine here. Go find something!")
        state.last_move = ' ' + state.move
        return

    available_choices = []
    print('Things you can examine:')
    for mob in state.creatures:
        if mob['room'] == current_room:
            print(mob['name'].capitalize())
            available_choices.append(mob['name'].lower())
    for thing in state.things:
        if thing['location'] == current_room and not thing['on_person']:
            print(thing['name'].capitalize())
            available_choices.append(thing['name'].lower())
    if state.inventory_quantity > 0:
        for thing in state.things:
            if thing['on_person']:
                print(thing['name'].capitalize())
                available_choices.append(thing['name'].lower())

    print('What do you want to examine? (type the name or press ENTER for none)')
    choice = input('Examine: ').lower()
    if choice == '':
        return
    while choice not in available_choices:
        print("That's not a valid choice. Try again.")
        print('What do you want to examine? (type the name or press ENTER for none)')
        choice = input('Examine: ').lower()
        if choice == '':
            return

    for thing in state.things:
        if thing['name'].lower() == choice:
            print(thing['description'])
            state.last_move = state.move + ' ' + choice
    for mob in state.creatures:
        if mob['name'].lower() == choice:
            if mob['is_dead']:
                print(mob['dead_description'])
            else:
                print(mob['description'] + '\n' + mob['name'] + ' '
                      + creature_wellness(mob['current_hp'], mob['max_hp']), end='')
                if mob['is_hostile']:
                    print(' ' + mob['status_hostile'])
                else:
                    print(' ' + mob['status_neutral'])
            state.last_move = state.move + ' ' + choice


def take_item(current_room, state):
    target = state.target

    if state.room_has_items:
        available_choices = [
            t['name'].lower() for t in state.things
            if t['location'] == current_room and not t['on_person']
        ]

        if target:
            for thing in state.things:
                if thing['name'].lower() == target.lower():
                    if thing['on_person']:
                        print('You already have the ' + thing['name'] + '.')
                        state.last_move = state.move + ' ' + target
                        return
                    if thing['moveable'] and thing['location'] == current_room:
                        thing['on_person'] = True
                        state.inventory_quantity += 1
                        print('You pick up the ' + thing['name'] + '.')
                        state.last_move = state.move + ' ' + target
                        return
                    else:
                        if thing['location'] != current_room:
                            print('What ' + thing['name'] + '?')
                        else:
                            print("You can't take the " + thing['name'] + '.')
                        return

        print('Items you see:')
        for name in available_choices:
            print(name.capitalize())
        print('What item do you want to take? (type the item name or press ENTER for none)')
        choice = input('Take: ').lower()
        if choice == '':
            return
        while choice not in available_choices:
            print("That's not a valid choice. Try again.")
            print('What item do you want to take? (type the item name or press ENTER for none)')
            choice = input('Take: ').lower()
            if choice == '':
                return
        for thing in state.things:
            if thing['name'].lower() == choice:
                if thing['moveable']:
                    thing['on_person'] = True
                    state.inventory_quantity += 1
                    print('You pick up the ' + thing['name'] + '.')
                    state.last_move = state.move + ' ' + choice
                else:
                    print("You can't take the " + thing['name'] + '.')
                    state.last_move = state.move + ' ' + choice
    else:
        if target:
            for thing in state.things:
                if thing['name'].lower() == target.lower() and thing['on_person']:
                    print('You already have the ' + thing['name'] + '.')
                    state.last_move = state.move + ' ' + target
                    return
        print("There aren't any items worth taking.")


def drop_item(current_room, state):
    target = state.target

    if state.inventory_quantity == 0:
        print("You aren't carrying anything.")
        return

    if target:
        if target in available_targets(current_room, state):
            for thing in state.things:
                if thing['name'].lower() == target.lower():
                    if not thing['on_person']:
                        print("You aren't carrying the " + thing['name'] + '.')
                    elif thing['no_drop']:
                        print("You can't drop the " + thing['name'] + '.')
                    else:
                        thing['on_person'] = False
                        thing['location'] = current_room
                        state.inventory_quantity -= 1
                        print('You drop the ' + thing['name'] + '.')
            state.last_move = state.move + ' ' + target
            return
        else:
            print('"' + target + '" is not in your inventory.')
            state.last_move = state.move + ' ' + target

    available_choices = [t['name'].lower() for t in state.things if t['on_person']]
    print('Items you are carrying:')
    for name in available_choices:
        print(name.capitalize())
    print('What item do you want to drop? (type the item name or press ENTER for none)')
    choice = input('Drop: ').lower()
    if choice == '':
        return
    while choice not in available_choices:
        print("That's not a valid choice. Try again.")
        print('What item do you want to drop? (type the item name or press ENTER for none)')
        choice = input('Drop: ').lower()
        if choice == '':
            return
    for thing in state.things:
        if thing['name'].lower() == choice:
            if thing['no_drop']:
                print("You can't drop the " + thing['name'] + '.')
            else:
                thing['on_person'] = False
                thing['location'] = current_room
                state.inventory_quantity -= 1
                print('You drop the ' + thing['name'] + '.')
                state.last_move = state.move + ' ' + choice


def use_item(current_room, state, world_module):
    target = state.target

    if target:
        if target in available_targets(current_room, state):
            _execute_use(target, current_room, state, world_module)
            state.last_move = state.move + ' ' + target
            return
        else:
            print('"' + target + '" is not available to use.')

    if not state.room_has_items and state.inventory_quantity == 0:
        print("There isn't anything you can use here.")
        return

    available_choices = []
    print('Items you can use:')
    if state.room_has_items:
        for thing in state.things:
            if thing['location'] == current_room and not thing['on_person']:
                print(thing['name'].capitalize())
                available_choices.append(thing['name'].lower())
    if state.inventory_quantity > 0:
        for thing in state.things:
            if thing['on_person']:
                print(thing['name'].capitalize())
                available_choices.append(thing['name'].lower())

    print('What item do you want to use? (type the item name or press ENTER for none)')
    choice = input('Use: ').lower()
    if choice == '':
        return
    while choice not in available_choices:
        print("That's not a valid choice. Try again.")
        print('What item do you want to use? (type the item name or press ENTER for none)')
        choice = input('Use: ').lower()
        if choice == '':
            return

    _execute_use(choice, current_room, state, world_module)
    state.last_move = state.move + ' ' + choice


def _execute_use(item_name, current_room, state, world_module):
    """Internal: apply weapon/defense/event logic for a chosen item."""
    is_weapon = weapon_checker(item_name, state)
    is_defense = defense_checker(item_name, state)

    if is_weapon:
        if is_defense:
            # Shell: 50% chance to just hide; otherwise fire any shell event
            if random.randrange(2) == 0:
                print('You hide in your shell.')
            else:
                check_event(item_name, current_room, state, world_module)
            creature_attack_block(current_room, state, world_module)
        else:
            pick_up_if_weapon(item_name, state)
            if attack_checker(current_room, state):
                check_event(item_name, current_room, state, world_module)
                player_attack(current_room, item_name, state, world_module)
            else:
                check_event(item_name, current_room, state, world_module)
            creature_attack(current_room, state)
    else:
        found = check_event(item_name, current_room, state, world_module)
        if not found:
            print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')
        creature_attack(current_room, state)


# ---------------------------------------------------------------------------
# Input / movement
# ---------------------------------------------------------------------------

def get_move(state):
    print('What do you want to do?')
    raw = input()
    state.target = extract_target(raw, state)
    verb = state.choice
    if verb.lower() in ('r', 'repeat'):
        repeated = repeat_move(state)
        return repeated if repeated else ''
    while verb.lower() not in ALLOWED_MOVES and verb.lower() not in ALLOWED_ACTIONS:
        print('"' + raw + '" is not recognized. Please try again.')
        print('What do you want to do?')
        raw = input()
        state.target = extract_target(raw, state)
        verb = state.choice
    return verb.lower()


def extract_target(command, state):
    space = command.find(' ')
    if space == -1:
        state.choice = command
        return ''
    state.choice = command[:space]
    return command[space + 1:]


def repeat_move(state):
    answer = input(f"Enter 'Y' or 'Yes' to repeat \"{state.last_move.lower()}\": ")
    if answer.lower() in ('y', 'yes'):
        state.choice = state.last_move.lower()
        state.target = extract_target(state.last_move, state)
        return state.choice
    return ''


def valid_move(from_room, direction, state):
    return direction in state.world[from_room]['exits']


def short_move(direction):
    if len(direction) == 9:          # 'northeast' / 'northwest' / 'southeast' / 'southwest'
        return direction[0] + direction[5]
    if direction == 'up':
        return 'u'
    if len(direction) == 2:
        return direction
    if len(direction) > 1:
        return direction[0]
    return direction


def full_direction(short_dir):
    return {
        'n':  'North     - ',
        's':  'South     - ',
        'e':  'East      - ',
        'w':  'West      - ',
        'u':  'Up        - ',
        'd':  'Down      - ',
        'ne': 'Northeast - ',
        'nw': 'Northwest - ',
        'se': 'Southeast - ',
        'sw': 'Southwest - ',
    }.get(short_dir, short_dir + ' - ')


# ---------------------------------------------------------------------------
# Game selection (setup)
# ---------------------------------------------------------------------------

def select_game():
    print('Choose a text game by number:')
    print('1 - OG Portal')
    print('2 - Combat practice')
    print('3 - Space adventure')
    print('4 - Lake Tortuga')
    print("If you want to continue a saved game, select the game by number then type 'load'.")
    choice = input('Your choice? ')
    while choice not in AVAILABLE_GAMES:
        print('Enter a number from the above list to choose a text game.')
        choice = input()
    return choice
