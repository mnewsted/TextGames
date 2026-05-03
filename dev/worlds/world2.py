"""
World 2 — Combat Practice

Data: room definitions, items, events, creatures (ROOMS, ITEMS, EVENTS, CREATURES).
Logic: handle_event() for all world-2-specific event side effects.

Replaces the choice == '2' block inside load_game() and do_event() in games.py.
"""

# handle_event references state.things, state.world, state.events, state.player_hp,
# and state.delete_thing() / state.add_thing(). Wired up in step 2 (GameState).

STARTING_ROOM = 0
EXIT_ROOM = 2
SAFE_ROOMS = []
SPECIAL_ROOMS = []
SPECIAL_DONE = []

INTRO_TEXT = (
    '*** Welcome to Combat practice ***\n\n'
    'This is just a small world to help you get used to combat.\n'
    "When you get tired of fighting, just drop into the pit.\n"
    "Unfortunately, the pit is covered by a locked grate. Who has the key?\n"
)

OUTRO_TEXT = 'Welp, you survived. The real challenge lies ahead.'

ROOMS = [
    {   # 0 - Start
        'visible': True, 'name': 'Start', 'prefix': 'at the', 'name2': '',
        'desc': 'This bare room is an octagon. You see a door in the southeast wall.',
        'exits': {'se': 1},
    },
    {   # 1 - Arena  (named 'Exit' in-game — the room with the pit)
        'visible': True, 'name': 'Exit', 'prefix': 'at the', 'name2': '',
        'desc': 'Packed dirt covers the floor of this spacious arena. A door is in the northwest corner. On the south wall, the words "EXIT BELOW" are painted in what could be dried blood. Or maybe ketchup? Below it is a large pit covered by an old grate.',
        'exits': {'nw': 0},
    },
    {   # 2 - End  (actual exit, exit_room)
        'visible': True, 'name': 'End', 'prefix': 'out the', 'name2': '',
        'desc': 'End description',
        'exits': {},
    },
]

ITEMS = [
    {
        'name': 'hammer', 'prefix': 'a',
        'description': "It's a classic ball-peen hammer. Could do some real damage.",
        'location': 0, 'on_person': False, 'moveable': True,
        'is_weapon': True, 'base_damage': 10, 'damage': 30, 'hit_bonus': 20, 'no_drop': False,
    },
    {
        'name': 'cog', 'prefix': 'a',
        'description': 'This rusty machine cog is worn down from years of use.',
        'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'elixir', 'prefix': 'an',
        'description': 'A small glass bottle contains a bright green liquid. The label reads: "Drink for fast-acting relief."',
        'location': 1, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'locked grate', 'prefix': 'a',
        'description': 'An ancient lattice of metal strips blocks access to the pit below, and sweet freedom. There is a large lock with a dusty keyhole holding the grate in place.',
        'location': 1, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
]

CREATURES = [
    {
        'id': 0, 'name': 'Monster',
        'description': 'The monster is about 7 feet tall, covered in yellow fur, and shows sharp teeth and claws.',
        'room': 0, 'max_hp': 100, 'current_hp': 100, 'is_dead': False, 'is_hostile': False,
        'status_neutral': "It isn't interested in you.",
        'status_hostile': "It's very mad at you.",
        'damage': 20, 'hit_bonus': 20, 'attack_chance': 75, 'is_fatigued': False,
        'death_event': 3,
        'was_seen': False,
        'dead_description': "The sharp teeth and claws of the monster aren't so scary now that it's dead.",
    },
]

# Event index == event ID.
# Note: events 2 and 3 were inserted out of order in games.py but resolve to the
# correct positions [0, 1, 2, 3]. Listed here in logical order.
EVENTS = [
    {   # 0 - Swing hammer (flavor text only; actual damage handled by combat system)
        'id': 0, 'done': False, 'room': 999, 'item_name': 'hammer',
        'first_time_text': 'You swing the hammer.',
        'already_done_text': 'You swing the hammer.',
    },
    {   # 1 - Drink elixir: heal 50 hp, leave empty bottle, remove elixir
        'id': 1, 'done': False, 'room': 999, 'item_name': 'elixir',
        'first_time_text': 'You open the bottle and gulp down the contents. It tastes like ecto-cooler. Regardless, you feel a surge of wellness in your body.',
        'already_done_text': 'The small bottle is empty. What a shame.',
    },
    {   # 2 - Use magic key on grate: reveal End room, update arena desc + exits, remove grate
        'id': 2, 'done': False, 'room': 1, 'item_name': 'magic key',
        'first_time_text': 'You have to force the magic key into the keyhole, but when you turn it, the lock mechanism cracks apart. The grate slides open revealing a surprisingly inviting hole in the ground.',
        'already_done_text': 'The pit is now accessible.',
    },
    {   # 3 - Monster death: drop magic key at monster's location (triggered by death_event)
        'id': 3, 'done': False, 'room': 999, 'item_name': 'magic key',
        'first_time_text': 'As the monster crumbles into a heap, a metallic object clangs onto the floor.',
        'already_done_text': 'Come on, think about it. You can figure this out.',
    },
]


def handle_event(event_id, current_room, state):
    """Execute the side effects for the given event id.

    Reads and writes: state.things, state.world, state.events, state.player_hp.
    Calls: state.delete_thing(name), state.add_thing(item_dict).
    Both are wired up in step 2 (GameState).
    """
    event = state.events[event_id]

    # --- Swing hammer: flavor text only ---
    if event_id == 0:
        print(event['first_time_text'])
        event['done'] = True

    # --- Drink elixir: heal, leave empty bottle, remove elixir ---
    elif event_id == 1:
        print(event['first_time_text'])
        event['done'] = True
        state.player_hp = min(state.player_hp + 50, 100)
        state.add_thing({
            'name': 'empty bottle', 'prefix': 'an',
            'description': 'Staring at the empty elixir bottle fills you with longing.',
            'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('elixir')

    # --- Magic key on grate: reveal End room, update arena desc + exits, remove grate ---
    elif event_id == 2:
        print(event['first_time_text'])
        event['done'] = True
        state.world[2]['visible'] = True
        state.world[1]['desc'] = 'Packed dirt covers the floor of this spacious arena. A door is in the northwest corner. On the south wall, the words "EXIT BELOW" are painted in what could be dried blood. Or maybe ketchup? Below it is a large pit. You could probably climb down into it.'
        state.world[1]['exits'] = {'nw': 0, 'd': 2}
        state.delete_thing('locked grate')

    # --- Monster death: drop magic key at death location ---
    elif event_id == 3:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'magic key', 'prefix': 'a',
            'description': 'The over-sized key is made of dark metal. It gives off a faint vibration.',
            'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })


def handle_special(current_room, state):
    """World 2 has no special room logic."""
    pass
