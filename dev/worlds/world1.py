"""
World 1 — OG Portal

Data: room definitions, items, events (ROOMS, ITEMS, EVENTS, CREATURES).
Logic: handle_event() for all world-1-specific event side effects.

Replaces the choice == '1' block inside load_game() and do_event() in games.py.
"""

# handle_event references state.things, state.world, state.events, and
# state.delete_thing(). These are wired up in step 2 (GameState).

STARTING_ROOM = 0
EXIT_ROOM = 5
SAFE_ROOMS = []
SPECIAL_ROOMS = []
SPECIAL_DONE = []

INTRO_TEXT = (
    '*** Welcome to OG Portal ***\n\n'
    'Well, this is odd. You find yourself in an unfamiliar house.\n'
    "You don't remember how you got here. You just know this isn't real.\n"
    'Look around and use things. If the way forward is not clear, keep looking. And using.\n\n'
    'You must escape and get back to reality!\n'
)

OUTRO_TEXT = 'Congratulations! You escaped that odd world and are back in reality.'

# Room index == room ID. 'name2' is a suffix appended to the room name on display (unused here).
ROOMS = [
    {   # 0 - House
        'visible': True, 'name': 'House', 'prefix': 'in the', 'name2': '',
        'desc': 'This modest dwelling has one room on the ground floor. You can see the front yard to the east and the garage through a door to the south. One set of stairs leads up to the studio, and another goes down to the basement.',
        'exits': {'e': 1, 's': 2, 'u': 8, 'd': 6},
    },
    {   # 1 - Yard
        'visible': True, 'name': 'Yard', 'prefix': 'in the', 'name2': '',
        'desc': 'The grass in the front yard is browning, and the flowers look sad. You can go west to back into the house, or go south around the house to the garage. Outside of the yard to the east is a street.',
        'exits': {'w': 0, 's': 2, 'e': 3},
    },
    {   # 2 - Garage
        'visible': True, 'name': 'Garage', 'prefix': 'in the', 'name2': '',
        'desc': "There is a musty smell, and oil stains cover the concrete floor. You can get to the house through the door to the north. The door to the yard is somehow stuck, but the main garage door to the east opens to the street.",
        'exits': {'n': 0, 'e': 3},
    },
    {   # 3 - Street
        'visible': True, 'name': 'Street', 'prefix': 'on the', 'name2': '',
        'desc': "You don't see any cars on this strikingly ordinary street. The house is nearby. To the north is the gate to the front yard, and the garage door is open to the west. You see a dusty junkyard to the east. Following the road south will bring you to a park.",
        'exits': {'n': 1, 'w': 2, 'e': 9, 's': 4},
    },
    {   # 4 - Park
        'visible': True, 'name': 'Park', 'prefix': 'at the', 'name2': '',
        'desc': 'The wide, grassy clearing at the end of the road is accented by a few tall trees. Part of the grass is bare along the southern edge, and it contains a strange etching of a house and a winged creature. The street is at the north end of the park, a trail leads through the trees to the west, and a small meadow is to the east.',
        'exits': {'n': 3, 'e': 10, 'w': 11},
    },
    {   # 5 - Glowy portal  (exit room, starts invisible)
        'visible': False, 'name': 'Glowy portal', 'prefix': 'through the', 'name2': '',
        'desc': 'End description',
        'exits': {},
    },
    {   # 6 - Basement
        'visible': True, 'name': 'Basement', 'prefix': 'in the', 'name2': '',
        'desc': 'It is really dark down here. And damp. Stairs lead back up into the house.',
        'exits': {'u': 0},
    },
    {   # 7 - Tree  (starts invisible, unlocked by planting tree kit)
        'visible': False, 'name': 'Tree', 'prefix': 'up a', 'name2': '',
        'desc': 'You climb to the upper branches of the newly sprouted tree.',
        'exits': {'d': 4},
    },
    {   # 8 - Studio
        'visible': True, 'name': 'Studio', 'prefix': 'in the', 'name2': '',
        'desc': "An old painting hangs on the wall of this small space. Another wall has a large print of abstract shapes inside a circle. If you squint, you think the shapes represent something flying out of a tall structure, or they could be a square lollipop barfing feathers. A stairway goes back down to the main room.",
        'exits': {'d': 0},
    },
    {   # 9 - Junkyard
        'visible': True, 'name': 'Junkyard', 'prefix': 'in the', 'name2': '',
        'desc': 'The air is thick in this run-down yard. Rusty scrap metal and mismatched tires are strewn about. The exit, back to the street, is on the west end of the junkyard.',
        'exits': {'w': 3},
    },
    {   # 10 - Meadow
        'visible': True, 'name': 'Meadow', 'prefix': 'in the', 'name2': '',
        'desc': 'This grassy spot is pleasant and wide. A lonely stone well sits in the middle. The park is to the west.',
        'exits': {'w': 4},
    },
    {   # 11 - Forest path
        'visible': True, 'name': 'Forest path', 'prefix': 'on the', 'name2': '',
        'desc': 'The dense woods are pierced by a well-worn trail. Looking west, the path appears to open into a dell. To the east, you see the park.',
        'exits': {'e': 4, 'w': 12},
    },
    {   # 12 - Dell
        'visible': True, 'name': 'Dell', 'prefix': 'in the', 'name2': '',
        'desc': 'This gentle valley is surrounded by leafy trees and bushes. A path is visible to the east, and to the north you see a sturdy iron gate that fills the only opening in the foliage.',
        'exits': {'e': 11},
    },
    {   # 13 - Winding passageway  (starts invisible, unlocked by key)
        'visible': False, 'name': 'Winding passageway', 'prefix': 'in a', 'name2': '',
        'desc': 'This jaunty tunnel is dimly lit by bioluminescent lichen. So pretty! The open iron gate is at the south end of the passage. As it bends to the northeast, it goes deeper and deeper into the earth.',
        'exits': {'s': 12, 'ne': 14},
    },
    {   # 14 - Subbasement
        'visible': True, 'name': 'Subbasement', 'prefix': 'in the', 'name2': '',
        'desc': "This tiny, chilly room opens west to a winding passageway. There's a trick one-way trapdoor in the ceiling, which you can access using handholds cut into the wall.",
        'exits': {'sw': 13, 'u': 6},
    },
]

ITEMS = [
    {
        'name': 'note', 'prefix': 'a',
        'description': "Something is badly scrawled on this yellowing paper, but with effort, you can read it. \n'If you don't like it here, exit through the portal.\nObviously, portals aren't naturally occurring.\nYou'll have to summon one.\nI think there's a clue in the studio.'",
        'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'pebble', 'prefix': 'a',
        'description': 'This tiny rock has been smoothed by eons of natural erosion. How could something so small be so old?',
        'location': 1, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'ball', 'prefix': 'a',
        'description': "It's a dark pink playground ball.",
        'location': 4, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'Mona Lisa', 'prefix': 'the',
        'description': 'This painting is a masterpiece of the Italian Renaissance. There is something to that smile.',
        'location': 8, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'tricycle', 'prefix': 'a',
        'description': "The light blue aluminum tricycle appears to be in working order, though that plastic seat doesn't seem comfortable.",
        'location': 3, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'tree kit', 'prefix': 'a',
        'description': "The tree kit box claims: 'Makes a real life tree in seconds! No digging required. For best results, use in an open area.'",
        'location': 2, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'egg', 'prefix': 'an',
        'description': "The small, blue egg feels weighty, like there's something inside it.",
        'location': 7, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'post', 'prefix': 'a',
        'description': "It's four feet tall, stuck in the ground, and has a little square table surface at the top.",
        'location': 1, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'machine', 'prefix': 'a',
        'description': 'You try to make sense of this large, well-maintained, metallic box. It is the size of a refrigerator but without any visible doors. It has two holes: a small slot near the top and a large square hole at the bottom.',
        'location': 9, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'broken well', 'prefix': 'a',
        'description': "It looks like this old well isn't completely broken. The crank turns, adjusting the height of the rope, but nothing is attached to it. At the bottom of the well, something reflects light back up to you.",
        'location': 10, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'bucket', 'prefix': 'a',
        'description': 'This yellow bucket has a wide handle at the top, making it easy to hold.',
        'location': 2, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'coin', 'prefix': 'a',
        'description': "This rusty coin has indecipherable symbols on one side and a rectangular shape on the other. It doesn't appear to be worth much.",
        'location': 13, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'gate', 'prefix': 'a',
        'description': 'This is a serious gate. The wrought-iron frame is elegant yet ominous. You see a bulky, brass lock mechanism that contains a happy keyhole.',
        'location': 12, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
]

CREATURES = []

# Event index == event ID. room 999 means the event can trigger in any room.
EVENTS = [
    {   # 0 - Mona Lisa winks
        'id': 0, 'done': False, 'room': 8, 'item_name': 'Mona Lisa',
        'first_time_text': 'Mona Lisa winks at you.',
        'already_done_text': "The portrait isn't doing anything else.",
    },
    {   # 1 - Ball in house
        'id': 1, 'done': False, 'room': 0, 'item_name': 'ball',
        'first_time_text': "Mom always said, 'Don't play ball in the house.'",
        'already_done_text': "Seriously, 'Don't play ball in the house.'",
    },
    {   # 2 - Plant tree (reveals room 7, updates park desc/exits)
        'id': 2, 'done': False, 'room': 4, 'item_name': 'tree kit',
        'first_time_text': "Though you can't find instructions, the tree kit is suprisingly easy to use. A huge tree shoots up from the earth.",
        'already_done_text': "The kit's reagents are all used up.",
    },
    {   # 3 - Crack egg (creates robin + egg shell, removes egg)
        'id': 3, 'done': False, 'room': 999, 'item_name': 'egg',
        'first_time_text': "You crack open the egg. A slimy robin emerges. It's shivering, so you put it in your pocket. The shell falls to your feet.",
        'already_done_text': "It's empty. There's little to do with the broken egg shell.",
    },
    {   # 4 - Ride tricycle
        'id': 4, 'done': False, 'room': 999, 'item_name': 'tricycle',
        'first_time_text': 'You ride the tricycle around and around. Whee!',
        'already_done_text': 'You ride the tricycle again. That fun never gets old.',
    },
    {   # 5 - Use flashlight in basement (reveals toy house)
        'id': 5, 'done': False, 'room': 6, 'item_name': 'flashlight',
        'first_time_text': 'You shine the flashlight across the room. A tiny toy house is now visible on the floor.',
        'already_done_text': "There's nothing surprising when you use the flashlight.",
    },
    {   # 6 - Place toy house on post (creates birdhouse, removes toy house)
        'id': 6, 'done': False, 'room': 1, 'item_name': 'toy house',
        "first_time_text": "You attach the toy house to the post. You've made a birdhouse!",
        'already_done_text': "It looks perfect where it is. There's nothing more to do with it.",
    },
    {   # 7 - Place robin in birdhouse (reveals portal, removes robin)
        'id': 7, 'done': False, 'room': 1, 'item_name': 'robin',
        'first_time_text': 'You place the baby robin into the birdhouse. You hear a loud but pleasant cracking sound in the distance to the east and a little south.',
        'already_done_text': 'The bird seems content already. Best leave it alone.',
    },
    {   # 8 - Ball in studio
        'id': 8, 'done': False, 'room': 8, 'item_name': 'ball',
        'first_time_text': "Mom always said, 'Don't play ball in the house.'",
        'already_done_text': "Seriously, 'Don't play ball in the house.'",
    },
    {   # 9 - Ball in basement
        'id': 9, 'done': False, 'room': 6, 'item_name': 'ball',
        'first_time_text': "Mom always said, 'Don't play ball in the house.'",
        'already_done_text': "Seriously, 'Don't play ball in the house.'",
    },
    {   # 10 - Ball at machine
        'id': 10, 'done': False, 'room': 9, 'item_name': 'ball',
        "first_time_text": "You try to fit the ball into the bigger round hole of the machine, but it doesn't fit.",
        'already_done_text': "Try as you might, you still can't get the ball into the machine.",
    },
    {   # 11 - Coin in machine (creates flashlight, removes coin)
        'id': 11, 'done': False, 'room': 9, 'item_name': 'coin',
        'first_time_text': 'You place the coin in the slot of the machine. It pings off metal within, causing gears to churn and grind. It goes silent for a few seconds, then a flashlight shoots out of the lower hole, narrowly missing your leg!',
        'already_done_text': "There's nothing more to do with it.",
    },
    {   # 12 - Ball anywhere else
        'id': 12, 'done': False, 'room': 999, 'item_name': 'ball',
        'first_time_text': 'You throw, catch, and bounce the ball. Fun stuff.',
        'already_done_text': 'You throw, catch, and bounce the ball some more. Fun stuff.',
    },
    {   # 13 - Read note
        'id': 13, 'done': False, 'room': 999, 'item_name': 'note',
        'first_time_text': "Something is badly scrawled on this yellowing paper, but with effort, you can read it. 'If you don't like it here, exit through the portal. Obviously, portals aren't naturally occurring. You'll have to summon one. I think there's a clue in the studio.'",
        'already_done_text': "Something is badly scrawled on this yellowing paper, but with effort, you can read it. 'If you don't like it here, exit through the portal. Obviously, portals aren't naturally occurring. You'll have to summon one. I think there's a clue in the studio.'",
    },
    {   # 14 - Examine post
        'id': 14, 'done': False, 'room': 1, 'item_name': 'post',
        'first_time_text': "The post doesn't do anything by itself. Try using another item near it.",
        'already_done_text': "The post doesn't do anything by itself. Try using another item near it.",
    },
    {   # 15 - Examine machine
        'id': 15, 'done': False, 'room': 9, 'item_name': 'machine',
        "first_time_text": "You can't figure out how to get the machine to do anything. Try using another item near it.",
        'already_done_text': "You can't figure out how to get the machine to do anything. Try using another item near it.",
    },
    {   # 16 - Use broken well (no bucket yet)
        'id': 16, 'done': False, 'room': 10, 'item_name': 'broken well',
        "first_time_text": "Turning the crank lowers the line into the water and back up again. There's definitely something shiny at the bottom of the well, but it's too narrow to climb down.",
        'already_done_text': "Turning the crank lowers the line into the water and back up again. There's definitely something shiny at the bottom of the well, but it's too narrow to climb down.",
    },
    {   # 17 - Attach bucket to well (creates functional well, removes broken well + bucket)
        'id': 17, 'done': False, 'room': 10, 'item_name': 'bucket',
        'first_time_text': 'You tie the rope around the bucket handle. You fixed the well!',
        'already_done_text': "Using the bucket now that it is attached doesn't do anything. Try something else?",
    },
    {   # 18 - Use well (creates key)
        'id': 18, 'done': False, 'room': 10, 'item_name': 'well',
        'first_time_text': 'By turning the crank, you lower the bucket into the well. It makes a small splash when it hits the bottom. You raise the bucket from the depths, and you see a moss covered key inside! You grab it, but it slips out of your hand onto the ground.',
        'already_done_text': "You lower and raise the bucket again, but you can't fish out anything else from the well.",
    },
    {   # 19 - Drop pebble in well (removes pebble)
        'id': 19, 'done': False, 'room': 10, 'item_name': 'pebble',
        'first_time_text': 'You drop the pebble in the well. It caroms off the stone side then splashes at the bottom. Bloop.',
        'already_done_text': "There's nothing more to do with it.",
    },
    {   # 20 - Use key on gate (reveals winding passageway)
        'id': 20, 'done': False, 'room': 12, 'item_name': 'key',
        'first_time_text': 'The key glides into the lock! With some effort, you turn the key and pull open the gate. An eerie light is coming from the cave to the north.',
        'already_done_text': 'Yep, the key still fits in the lock.',
    },
]


def handle_event(event_id, current_room, state):
    """Execute the side effects for the given event id.

    Reads and writes: state.things, state.world, state.events.
    Calls: state.delete_thing(name), state.add_thing(item_dict).
    Both are wired up in step 2 (GameState).
    """
    event = state.events[event_id]

    # --- Simple events: print text and mark done ---
    if event_id in [0, 1, 4, 8, 9, 10, 12, 13, 14, 15, 16]:
        print(event['first_time_text'])
        event['done'] = True

    # --- Plant tree: reveal tree room, update park desc + exits, update tree kit desc ---
    elif event_id == 2:
        print(event['first_time_text'])
        event['done'] = True
        state.world[7]['visible'] = True
        state.world[4]['desc'] = 'The grassy clearing at the end of the road is accented by a few tall trees. A new tree in the center has low, inviting branches. Part of the grass is bare along the southern edge, and it contains a strange etching of a house and a winged creature. The street is at the north end of the park, a trail leads through the trees to the west, and a meadow is to the east.'
        state.world[4]['exits'] = {'n': 3, 'u': 7, 'e': 10, 'w': 11}
        kit = next(t for t in state.things if 'tree kit' in t['name'])
        kit['description'] = "The empty tree kit box claims: 'Makes a real life tree in seconds! No digging required. For best results, use in an open area.'"

    # --- Crack egg: add robin to inventory, leave egg shell, remove egg ---
    elif event_id == 3:
        print(event['first_time_text'])
        event['done'] = True
        state.add_thing({
            'name': 'robin', 'prefix': 'a',
            'description': "Its feathers are matted down by egg goo, and the baby bird is struggling to open its tiny eyes. It would be gross if it weren't so darn cute.",
            'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })
        state.things.append({
            'name': 'egg shell', 'prefix': 'an',
            'description': "There's little to do with the broken egg shell shards.",
            'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('egg')

    # --- Use flashlight in basement: reveal toy house ---
    elif event_id == 5:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'toy house', 'prefix': 'a',
            'description': 'This miniature colonial appears to be worn from play. You can imagine dolls going in and out of the doors and windows.',
            'location': 6, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })

    # --- Place toy house on post: create birdhouse, remove toy house ---
    elif event_id == 6:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'birdhouse', 'prefix': 'a',
            'description': 'The toy house resting atop the post will surely attract small, avian creatures.',
            'location': 1, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('toy house')

    # --- Place robin in birdhouse: reveal portal, update park desc + exits, remove robin ---
    elif event_id == 7:
        if any(t['name'] == 'birdhouse' for t in state.things):
            print(event['first_time_text'])
            event['done'] = True
            state.world[5]['visible'] = True
            state.world[4]['desc'] = 'The grassy clearing at the end of the road is dappled with light shining through the tall trees. A new tree in the center has low, inviting branches. Where the grass was worn to the south, you now see a brightly glowing portal! The street is at the north end of the park, a trail leads through the trees to the west, and a meadow is to the east.'
            state.world[4]['exits'] = {'n': 3, 'u': 7, 's': 5}
            state.delete_thing('robin')
        else:
            print('Nothing happened.')

    # --- Coin in machine: create flashlight, remove coin ---
    elif event_id == 11:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'flashlight', 'prefix': 'a',
            'description': "It's your standard issue flashlight. Looks like it could help you see in dark places, but it wouldn't do much elsewhere.",
            'location': 9, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('coin')

    # --- Attach bucket to well: create functional well, remove broken well + bucket ---
    elif event_id == 17:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'well', 'prefix': 'the',
            'description': 'The well is still old, but now you can raise and lower the bucket.',
            'location': 10, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('broken well')
        state.delete_thing('bucket')

    # --- Use well: create key on ground ---
    elif event_id == 18:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'key', 'prefix': 'a',
            'description': 'The brass key is partially covered in moss. It feels heavy.',
            'location': 10, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })

    # --- Drop pebble in well: remove pebble ---
    elif event_id == 19:
        print(event['first_time_text'])
        event['done'] = True
        state.delete_thing('pebble')

    # --- Use key on gate: reveal winding passageway, update dell desc + exits ---
    elif event_id == 20:
        print(event['first_time_text'])
        event['done'] = True
        state.world[13]['visible'] = True
        state.world[12]['desc'] = 'This gentle valley is surrounded by leafy trees and bushes. A path is visible to the west. To the north you see an open iron gate, beyond which lies the mouth of a cave.'
        state.world[12]['exits'] = {'e': 11, 'n': 13}


def handle_special(current_room, state):
    """World 1 has no special room logic."""
    pass
