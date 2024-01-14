#! python3
# TextGames Combat Practice - Game 2
# version 1.0
# description: separated code

def do_event(event_id, current_room):
    global inventory_quantity
    global game_choice
    global player_hp

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

# unused function
def do_special(current_room):
    return

world = []
things = []
events = []
creatures = []
special_rooms = []
special_done = []

starting_room = 0
exit_room = 2
player_hp = 100

intro_text = '*** Welcome to Combat practice ***\n\nThis is just a small world to help you get used to combat.\nWhen you get tired of fighting, just drop into the pit.\n'
outro_text = 'Welp, you survived. The real challenge lies ahead.'

world.insert(0, {'visible': True, 'name': 'Start', 'prefix': 'at the', 'name2': '',
                 'desc': 'This bare room is an octagon. You see a door in the southeast wall.',
                 'exits': {'se': 1}})
world.insert(1, {'visible': True, 'name': 'End', 'prefix': 'at the', 'name2': '',
                 'desc': 'Packed dirt covers the floor of this spacious arena. A door is in the northwest corner. On the south wall, the word "EXIT" is painted in what could be dried blood. Or maybe ketchup? Below it is a large pit. You could probably climb down into it.',
                 'exits': {'nw': 0, 'd': 2}})
world.insert(2, {'visible': True, 'name': 'Exit', 'prefix': 'out the', 'name2': '', 'desc': 'End description',
                 'exits': {}})

things.append({'name': 'hammer', 'prefix': 'a',
               'description': 'It\'s a classic ball-peen hammer. Could do some real damage.', 'location': 0,
               'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': 10, 'damage': 30,
               'hit_bonus': 20})
things.append({'name': 'cog', 'prefix': 'a', 'description': 'This rusty machine cog is worn down from years of use.',
               'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': False})
things.append({'name': 'elixir', 'prefix': 'an',
               'description': 'A small glass bottle contains a bright green liquid. The label reads: "Drink for fast-acting relief."',
               'location': 1, 'on_person': False, 'moveable': True, 'is_weapon': False})

events.insert(0, {'id': 0, 'done': False, 'room': 999, 'item_name': 'hammer',
                  'first_time_text': 'You swing the hammer.', 'already_done_text': 'You swing the hammer.'})
events.insert(1, {'id': 1, 'done': False, 'room': 1, 'item_name': 'elixir',
                  'first_time_text': 'You open the bottle and gulp down the contents. It tastes like ecto-cooler. Regardless, you feel a surge of wellness in your body.',
                  'already_done_text': 'The small bottle is empty. What a shame.'})
creatures.append({'id': 0, 'name': 'Monster',
                  'description': 'The monster is about 7 feet tall, covered in yellow fur, and shows sharp teeth and claws.',
                  'room': 0, 'max_hp': 100, 'current_hp': 100, 'is_dead': False, 'is_hostile': False,
                  'status_neutral': 'It isn\'t interested in you.', 'status_hostile': 'It\'s very mad at you.',
                  'damage': 20, 'hit_bonus': 20, 'attack_chance': 75, 'is_fatigued': False, 'death_event': 0,
                  'was_seen': False,
                  'dead_description': 'The sharp teeth and claws of the monster aren\'t so scary now that it\'s dead.'})

# unused vars
special_rooms = []
special_done = []
launch_code = ''
