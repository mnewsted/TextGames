"""
World 3 — Space Adventure

Data: room definitions, items, events, creatures (ROOMS, ITEMS, EVENTS, CREATURES).
Logic: handle_event() for all world-3-specific event side effects,
       including the launch code checker and bad-air damage special.

Replaces the choice == '3' block inside load_game(), do_event(), and
do_special() in games.py.
"""

import random
from combat import player_wellness

STARTING_ROOM = 0
EXIT_ROOM = 99
SAFE_ROOMS = []
SPECIAL_ROOMS = list(range(5, 50))
SPECIAL_DONE = [{'id': 0, 'done': False}, {'id': 1, 'done': False}]
LAUNCH_CODE = ''

INTRO_TEXT = (
    '*** Welcome to Space adventure ***\n\n'
    "You are on the custodial crew of an intergalactic starship. Your ship's mission was to respond to a distress signal sent by another ship in a newly discovered planetary system.\n"
    'While happily cleaning the lounge, you overheard that something got into the ship. The last thing you remember was getting hit hard on the head.\n\n'
    'You awake in a locked cell...\n'
)

OUTRO_TEXT = (
    'The escape pod instruments light up, and you feel the machinery around the pod shifting, preparing for launch. You buckle into a seat as you watch the launch bay doors open outside the pod.'
    '\n\nThe thrusters blast and the pod hurtles out of the ship. Deepspace Communications systems are active in the pod, and you start sending a distress call to be picked up.'
    '\n\nCongratulations! You did it!'
)

ROOMS = [
    {   # 0 - Cell
        'visible': True, 'name': 'Cell', 'prefix': 'in a', 'name2': '',
        'desc': 'This cell has a single door to the north.',
        'exits': {'n': 1},
    },
    {   # 1 - Detention hallway
        'visible': True, 'name': 'Detention hallway', 'prefix': 'in the', 'name2': '',
        'desc': 'This long hallway has an elevator bay to the west. The hallway continues to the east. There is an open cell to the south.',
        'exits': {'w': 4, 'e': 2, 's': 0},
    },
    {   # 2 - Back hallway
        'visible': True, 'name': 'Back hallway', 'prefix': 'in the', 'name2': '',
        'desc': 'This is the end of the detention hallway. Back west is the main hallway. A small doorway is on the north wall.',
        'exits': {'w': 1, 'n': 3},
    },
    {   # 3 - Storage nook
        'visible': True, 'name': 'Storage nook', 'prefix': 'in a', 'name2': '',
        'desc': 'The only exit from this room is south.',
        'exits': {'s': 2},
    },
    {   # 4 - Detention Level Elevator Bay
        'visible': True, 'name': 'Detention Level Elevator Bay', 'prefix': 'at the', 'name2': ' (to Main Deck)',
        'desc': 'The elevator goes up to the Main Deck, but it requires a keycard to activate it. The detention hallway is to the east.',
        'exits': {'e': 1},
    },
    {   # 5 - Main Deck Elevator Bay 5 (hidden until detention elevator unlocked)
        'visible': False, 'name': 'Main Deck Elevator Bay 5', 'prefix': 'at', 'name2': ' (to Detention Level)',
        'desc': 'The elevator goes down to the Detention Level. To the west is a security checkpoint.',
        'exits': {'w': 6, 'd': 4},
    },
    {   # 6 - Main Deck Security Desk
        'visible': True, 'name': 'Main Deck Security Desk', 'prefix': 'at a', 'name2': '',
        'desc': 'This is the Main Deck Security Checkpoint. To the east is an elevator bay to the Detention Level. To the south is an elevator bay to the Engine Room. A walkway is visible to the west.',
        'exits': {'e': 5, 's': 7, 'w': 8},
    },
    {   # 7 - Main Deck Elevator Bay 4
        'visible': True, 'name': 'Main Deck Elevator Bay 4', 'prefix': 'at', 'name2': ' (to Engine Room)',
        'desc': 'The elevator goes down to the Engine Room. To the north is a security checkpoint.',
        'exits': {'n': 6, 'd': 14},
    },
    {   # 8 - Walkway
        'visible': True, 'name': 'Walkway', 'prefix': 'in the', 'name2': '',
        'desc': 'This walkway connects the Main Deck Security Desk to the East and a wide hallway to the West. North is an elevator bay to the Hangar.',
        'exits': {'e': 6, 'n': 9, 'w': 10},
    },
    {   # 9 - Main Deck Elevator Bay 3
        'visible': True, 'name': 'Main Deck Elevator Bay 3', 'prefix': 'at', 'name2': ' (to Hangar)',
        'desc': 'The elevator goes down to the Hangar, but it is currently deactivated. To the south is a walkway.',
        'exits': {'s': 8},
    },
    {   # 10 - Wide hallway
        'visible': True, 'name': 'Wide hallway', 'prefix': 'in the', 'name2': '',
        'desc': 'This wide hallway branches in several directions. To the east is a walkway. South is an elevator to the Armory. To the west, the hallway continues toward the front of the ship.',
        'exits': {'e': 8, 's': 11, 'w': 12},
    },
    {   # 11 - Main Deck Elevator Bay 2
        'visible': True, 'name': 'Main Deck Elevator Bay 2', 'prefix': 'at', 'name2': ' (to Armory)',
        'desc': 'The elevator goes down to the Armory. The control panel requires a retina scan to activate. To the north is a wide, branching hallway.',
        'exits': {'n': 10},
    },
    {   # 12 - Funneling hallway
        'visible': True, 'name': 'Funneling hallway', 'prefix': 'in a', 'name2': '',
        'desc': 'The hallway narrows as it leads from east to west. At the east end is a wide, branching hallway. To the west is an elevator to the Crew Quarters. '
                'Hardly visible in the southwest corner of the room is a dim passage to the Custodial Supplies room.',
        'exits': {'e': 10, 'w': 13, 'sw': 48},
    },
    {   # 13 - Main Deck Elevator Bay 1
        'visible': True, 'name': 'Main Deck Elevator Bay 1', 'prefix': 'at', 'name2': ' (to Quarters)',
        'desc': 'The elevator goes down to Crew Quarters, but it requires a keycard to activate it. To the east is a widening hallway.',
        'exits': {'e': 12},
    },
    {   # 14 - Engine Room Elevator Bay
        'visible': True, 'name': 'Engine Room Elevator Bay', 'prefix': 'at the', 'name2': ' (to Main Deck)',
        'desc': 'The elevator goes up to the Main Deck. To the east is the Engine Room.',
        'exits': {'u': 7, 'e': 15},
    },
    {   # 15 - Engine Room
        'visible': True, 'name': 'Engine Room', 'prefix': 'in the', 'name2': '',
        'desc': 'The loud, pusling motor fills up most of the room. To the north and south are fuel cell storage rooms. An equipment room is to the east. To the west is an elevator bay.',
        'exits': {'n': 16, 'e': 17, 's': 18, 'w': 14},
    },
    {   # 16 - North fuel cell storage
        'visible': True, 'name': 'North fuel cell storage', 'prefix': 'in the', 'name2': '',
        'desc': 'This room is filled with unused fuel cells. The only exit is to the south.',
        'exits': {'s': 15},
    },
    {   # 17 - Engine Equipment Room
        'visible': True, 'name': 'Engine Equipment Room', 'prefix': 'in the', 'name2': '',
        'desc': 'Spare parts, tools, and complex monitoring consoles fill this room. To the west is the engine room.',
        'exits': {'w': 15},
    },
    {   # 18 - South fuel cell storage
        'visible': True, 'name': 'South fuel cell storage', 'prefix': 'in the', 'name2': '',
        'desc': 'This room is filled with empty fuel cells. The only exit is to the north.',
        'exits': {'n': 15},
    },
    {   # 19 - Hangar Elevator Bay (hidden until override lever used)
        'visible': True, 'name': 'Hangar Elevator Bay', 'prefix': 'at the', 'name2': ' (to Main Deck)',
        'desc': 'The elevator goes up to the Main Deck. To the east is a wide entrance to the Hangar.',
        'exits': {'u': 9, 'e': 20},
    },
    {   # 20 - Hangar
        'visible': True, 'name': 'Hangar', 'prefix': 'in the', 'name2': '',
        'desc': 'This large room contains supply crates and a small, disassembled starship. Escape pods are in the southeast and southwest corners of the room. To the west is the elevator bay.',
        'exits': {'w': 19, 'se': 21, 'sw': 22},
    },
    {   # 21 - Escape pod B14
        'visible': True, 'name': 'Escape pod B14', 'prefix': 'in', 'name2': '',
        'desc': 'This small pod is surprisingly comfortable. The exit to the Hangar is to the northwest.',
        'exits': {'nw': 20},
    },
    {   # 22 - Escape pod L07
        'visible': True, 'name': 'Escape pod L07', 'prefix': 'in', 'name2': '',
        'desc': 'This small pod is cozy. The exit to the Hangar is to the northeast.',
        'exits': {'ne': 20},
    },
    {   # 23 - Armory Elevator Bay
        'visible': True, 'name': 'Armory Elevator Bay', 'prefix': 'at the', 'name2': ' (to Main Deck)',
        'desc': 'This elevator goes up to the Main Deck. To the south is a security checkpoint.',
        'exits': {'u': 11, 's': 24},
    },
    {   # 24 - Armory Security Desk
        'visible': True, 'name': 'Armory Security Desk', 'prefix': 'at the', 'name2': '',
        'desc': 'This is the heavily-fortified Armory Security Desk. To the east is the Guard Auxilary. To the north is an elevator bay.',
        'exits': {'n': 23, 'e': 25},
    },
    {   # 25 - Guard Auxilary
        'visible': True, 'name': 'Guard Auxilary', 'prefix': 'in the', 'name2': '',
        'desc': 'The scent of battle is inescapable. Two storage rooms are accessible: Weapons to the north and Supplies to the east. The security checkpoint is to the west.',
        'exits': {'w': 24, 'n': 26, 'e': 27},
    },
    {   # 26 - Weapons storage room
        'visible': True, 'name': 'Weapons storage room', 'prefix': 'in the', 'name2': '',
        'desc': 'Implements of destruction fill every corner of this room. Most of them are beyond understanding. The only exit is south.',
        'exits': {'s': 25},
    },
    {   # 27 - Armory supply room
        'visible': True, 'name': 'Armory supply room', 'prefix': 'in the', 'name2': '',
        'desc': 'This room contains many strange devices on shelving units and in closets. The exit is to the west.',
        'exits': {'w': 25},
    },
    {   # 28 - Quarters Elevator Bay 3 (hidden until quarters keycard used)
        'visible': False, 'name': 'Quarters Elevator Bay 3', 'prefix': 'at', 'name2': ' (to Main Deck)',
        'desc': 'This elevator goes up to the Main Deck. To the north is the lounge.',
        'exits': {'n': 29, 'u': 13},
    },
    {   # 29 - Lounge
        'visible': True, 'name': 'Lounge', 'prefix': 'in the', 'name2': '',
        'desc': 'The lounge is perfect for resting and recreation. Tables, comfy chairs, and several entertainment consoles are thoughtfully arranged. A wide observation deck is visible to the west. To the east is the dormitory. An elevator to the Main Deck is at the south end of the room.',
        'exits': {'s': 28, 'w': 32, 'e': 30},
    },
    {   # 30 - Dormitory
        'visible': True, 'name': 'Dormitory', 'prefix': 'in the', 'name2': '',
        'desc': 'Rows and rows of empty sleeping pods fill the room. To the east are what look like grooming facilities. The lounge is accessible to the west.',
        'exits': {'w': 29, 'e': 31},
    },
    {   # 31 - Crew Facilities
        'visible': True, 'name': 'Crew Facilities', 'prefix': 'in the', 'name2': '',
        'desc': 'Showers, steampods, and hygiene facilities are arranged to maximize privacy. There are a few odd items left in a ransacked supply closet. '
                'Rooms with toilets are to the north and south. The dormitory is to the west.',
        'exits': {'n': 46, 's': 47, 'w': 30},
    },
    {   # 32 - Observation Deck
        'visible': True, 'name': 'Observation Deck', 'prefix': 'in the', 'name2': '',
        'desc': 'A floor-to-ceiling window fills the western wall, giving a breathtaking view of the stars before the ship. Tables and seating are positioned to provide a relaxing sight. '
                'Elevator bays are on each end of the large window. An elevator to the bridge is to the north, and an elevator to the mess hall & medical services is to the south. To the east is the lounge area.',
        'exits': {'n': 33, 'e': 29, 's': 34},
    },
    {   # 33 - Quarters Elevator Bay 1
        'visible': True, 'name': 'Quarters Elevator Bay 1', 'prefix': 'at', 'name2': ' (to Bridge)',
        'desc': 'This elevator goes up to the Bridge, but it requires a keycard to activate it. To the south is the observation deck.',
        'exits': {'s': 32},
    },
    {   # 34 - Quarters Elevator Bay 2
        'visible': True, 'name': 'Quarters Elevator Bay 2', 'prefix': 'at', 'name2': ' (to Mess & Medical)',
        'desc': 'This elevator goes down to the Mess Hall and Medical Services, but it requires a keycard to activate it. The observation deck is to the north.',
        'exits': {'n': 32},
    },
    {   # 35 - Mess Hall and Medical Services Elevator Bay (hidden until mess keycard used)
        'visible': True, 'name': 'Mess Hall and Medical Services Elevator Bay', 'prefix': 'at the', 'name2': ' (to Quarters)',
        'desc': 'This elevator goes up to the Crew Quarters. To the east is the mess hall. South is a room called Medical Services A.',
        'exits': {'e': 38, 's': 36, 'u': 34},
    },
    {   # 36 - Medical Services A
        'visible': True, 'name': 'Medical Services A', 'prefix': 'in', 'name2': '',
        'desc': 'There is a small waiting area and a desk. To the north is an elevator bay. East is a room labeled Medical Services B.',
        'exits': {'n': 35, 'e': 37},
    },
    {   # 37 - Medical Services B
        'visible': True, 'name': 'Medical Services B', 'prefix': 'in', 'name2': '',
        'desc': 'Several cubbies with desks and chairs are situated in each corner. The east wall is filled with cabinets and drawers. The only exit is to the west.',
        'exits': {'w': 36},
    },
    {   # 38 - Mess Hall
        'visible': True, 'name': 'Mess Hall', 'prefix': 'in the', 'name2': '',
        'desc': 'This large room has neat rows of tables and a service area. The kitchen entrance is next to the service area on the north wall. Large double-doors connect a storage closet to the east. An elevator bay is to the west.',
        'exits': {'n': 39, 'e': 41, 'w': 35},
    },
    {   # 39 - Kitchen
        'visible': True, 'name': 'Kitchen', 'prefix': 'in the', 'name2': '',
        'desc': 'All kinds of food preparation and preservation devices are visible. A service area and doorway to the mess hall is to the south. The east wall connects to a deep walk-in pantry.',
        'exits': {'s': 38, 'e': 40},
    },
    {   # 40 - Pantry
        'visible': True, 'name': 'Pantry', 'prefix': 'in the', 'name2': '',
        'desc': 'Dry and packaged foodstuffs in boxes, bins, and bags line the shelves. A cold-storage unit is built into the north wall. To the west is the kitchen.',
        'exits': {'w': 39},
    },
    {   # 41 - Storage and cleaning closet
        'visible': True, 'name': 'Storage and cleaning closet', 'prefix': 'in the', 'name2': '',
        'desc': "This well-stocked closet holds dining implements, cleaning solutions, and scrubbing mechanisms. There's also a cabinet of tools. The mess hall is to the west.",
        'exits': {'w': 38},
    },
    {   # 42 - Bridge Elevator Bay
        'visible': True, 'name': 'Bridge Elevator Bay', 'prefix': 'at the', 'name2': ' (to Quarters)',
        'desc': 'This elevator goes down to the Crew Quarters. To the north is a security checkpoint.',
        'exits': {'d': 33, 'n': 43},
    },
    {   # 43 - Bridge Security Desk
        'visible': True, 'name': 'Bridge Security Desk', 'prefix': 'at the', 'name2': '',
        'desc': 'This is the bridge-level security desk. A door to the bridge is to the west, but it is shut. To the east is the Systems Control room. South is an elevator bay.',
        'exits': {'e': 45, 's': 42},
    },
    {   # 44 - Bridge (hidden until captain dies)
        'visible': False, 'name': 'Bridge', 'prefix': 'on the', 'name2': '',
        'desc': 'Even though it is called a bridge, it is more like a glorified cockpit. Flight controls and communications consoles are positioned near the officer chairs. East is the security desk.',
        'exits': {'e': 43},
    },
    {   # 45 - Systems Control room
        'visible': True, 'name': 'Systems Control room', 'prefix': 'in the', 'name2': '',
        'desc': "Data from the ship's environment control, propulsion, and weapons systems are a few of things displayed on huge screens in this room. The only way out is west to the security desk.",
        'exits': {'w': 43},
    },
    {   # 46 - Toilet Bank 1
        'visible': True, 'name': 'Toilet Bank 1', 'prefix': 'in', 'name2': '',
        'desc': 'An impressive number of toilets and bidets are discretely concealed within ceiling-to-floor privacy screens. The Crew Facilities are accessible to the south.',
        'exits': {'s': 31},
    },
    {   # 47 - Toilet Bank 2
        'visible': True, 'name': 'Toilet Bank 2', 'prefix': 'in', 'name2': '',
        'desc': 'An impressive number of toilets and bidets are discretely concealed within ceiling-to-floor privacy screens. The Crew Facilities are accessible to the north.',
        'exits': {'n': 31},
    },
    {   # 48 - Custodial Supplies room
        'visible': True, 'name': 'Custodial Supplies room', 'prefix': 'in the', 'name2': '',
        'desc': 'This dingy space contains an array of maintenance tools and equipment. To the northeast is the Funneling hallway. On the west side of the room is a door marked Workroom. '
                'It is locked, but the door knob has an old-fashioned keyhole in it.',
        'exits': {'ne': 12},
    },
    {   # 49 - Workroom (hidden until metal key used)
        'visible': False, 'name': 'Workroom', 'prefix': 'in the', 'name2': '',
        'desc': 'The familiar workroom has decent lighting and ample space to fix or build all kinds of things. '
                'The only exit is back east to the Custodial Supplies room.',
        'exits': {'e': 48},
    },
]

ITEMS = [
    {
        'name': 'food tray', 'prefix': 'a',
        'description': 'The empty food tray has some heft to it. The metal edge looks mean.',
        'location': 0, 'on_person': False, 'moveable': True,
        'is_weapon': True, 'base_damage': 10, 'damage': 10, 'hit_bonus': 25, 'no_drop': False,
    },
    {
        'name': 'stimpack', 'prefix': 'a',
        'description': 'A small vial of clear liquid has a tiny needle on one end and a red heart decal on the side.',
        'location': 3, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'breathing mask', 'prefix': 'a',
        'description': 'The compact device looks like it would fit nicely on your face if you pick it up or use it.',
        'location': 3, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'digipad1', 'prefix': 'a',
        'description': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                       '\n\tAfter we were attacked, I dragged you in here and set the door to lock from the inside.'
                       '\n\tYou can get out but be careful: most of the crew is dead. Those that survived are, well, dangerous.'
                       '\n\tUse whatever you can to survive. You gotta get off this ship. -B',
        'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'digipad2', 'prefix': 'a',
        'description': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                       "\n\tSome kind of virus swept through the ship. It killed most of the crew. Others were corrupted."
                       "\n\tThey do not need oxygen. They are diverting the ship's oxygen for some other purpose."
                       '\n\tI preserved the atmosphere settings on the Detention Level, but other places on the ship are probably bad. -B',
        'location': 2, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'wrench', 'prefix': 'a',
        'description': 'The heavy tool is rusted, but it could do some real damage.',
        'location': 17, 'on_person': False, 'moveable': True,
        'is_weapon': True, 'base_damage': 15, 'damage': 15, 'hit_bonus': 30, 'no_drop': False,
    },
    {
        'name': 'fuel cell', 'prefix': 'a',
        'description': 'This metallic cylinder emits a strange bluish glow from a slit on each end. A warning label reads: DANGER - Will burn through organic matter.',
        'location': 16, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'corpse', 'prefix': 'a',
        'description': 'The body of one of your crewmates lies on the floor, contorted in an unnatural pose. Every inch of their body is covered in a wet, dark gray-green substance. '
                       'It is translucent and looks hard, almost stone-like.',
        'location': 10, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'digipad5', 'prefix': 'a',
        'description': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                       "\n\tThe virus doesn't act the same on everybody. It doesn't make sense."
                       '\n\tI saw Jackson from Combat Services collapse. When she did, a jade crystal coating formed over her skin.'
                       '\n\tOthers went into zombie mode and started attacking. -A',
        'location': 8, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'allen claw', 'prefix': 'an',
        'description': 'This shiny, angular piece of metal appears to have been fashioned for a specific purpose.',
        'location': 41, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'smooth bar', 'prefix': 'a',
        'description': 'This rod is painted orange. It has fittings on both ends.',
        'location': 31, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'gummy grip', 'prefix': 'a',
        'description': 'The short pipe has a cushioned yet tackified surface.',
        'location': 27, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'dented tricorder', 'prefix': 'a',
        'description': 'This banged-up scanner must be good for something. It still beeps!',
        'location': 32, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'lockbox', 'prefix': 'a',
        'description': 'There are cryptic symbols on this oblong box. The lid is fastened tight, but a square keyhole looks promising.',
        'location': 18, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'scalpel', 'prefix': 'a',
        'description': 'The surgical blade is short but exceedingly sharp. It would be very effective at a targeted procedure, but it could also do some damage in a fight if it connected.',
        'location': 37, 'on_person': False, 'moveable': True,
        'is_weapon': True, 'base_damage': 10, 'damage': 25, 'hit_bonus': 15, 'no_drop': False,
    },
    {
        'name': 'fallen soldier', 'prefix': 'a',
        'description': 'This dead crewmate is bent backwards, leaning on the countertop. They have the insignia and fatigues of a tactical combat specialist. '
                       'Unlike the other bodies you encountered, this one seems frozen in shock, face up with eyes and mouth wide open.',
        'location': 39, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'large stimpack', 'prefix': 'a',
        'description': 'This device has 3 compact barrels of clear liquid that funnel into a small needle. You are comforted by the cheerful red heart logo on the top, '
                       'and the encouraging label that reads, "Massive vitality boost."',
        'location': 36, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'digipad4', 'prefix': 'a',
        'description': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                       "\n\tThey say you can see it in the eyes when they're infected. They get all hazy."
                       "\n\tIf that's true, then it's happening to me. I can't see my own reflection any more. -L",
        'location': 38, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'hot sauce', 'prefix': 'a',
        'description': 'This small bottle has a picture of a burning crescent-shaped pepper. "One drop\'ll do ya!"',
        'location': 40, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'mayonnaise', 'prefix': 'a',
        'description': 'The large jar of eggy, white, goop is still half-full.',
        'location': 40, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'pear powder', 'prefix': 'a',
        'description': 'A hand-written label on this see-through bag describes the sparkly, yellow granules inside the flavor pouch.',
        'location': 40, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'digipad3', 'prefix': 'a',
        'description': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                       '\n\tTraining today in Systems Control. Learned how to activate locked down systems.'
                       '\n\tThey got some real Rube Goldberg protocols. The lever that works the controls is'
                       '\n\tassembled from three parts in storage on the ship. How is that secure? -M',
        'location': 29, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'phaser', 'prefix': 'a',
        'description': 'The V-8 phaser pistol is a reliable mid- to close-range weapon.',
        'location': 26, 'on_person': False, 'moveable': True,
        'is_weapon': True, 'base_damage': 20, 'damage': 25, 'hit_bonus': 40, 'no_drop': False,
    },
    {
        'name': 'wound salve', 'prefix': 'a',
        'description': 'The label on the opaque brown jar reads, "Apply liberally to cuts, welts, and lacerations." Inside is a substance that looks like pink jelly.',
        'location': 27, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'digipad8', 'prefix': 'a',
        'description': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                       '\n\tThose infected, zombies, whatever--they do not stop.'
                       "\n\tMe and Barb held off 6 of them in the mess hall. Don't know why but food seemed to make them weak."
                       '\n\tOr maybe it just distracted them. Hope somebody sees this. -X',
        'location': 24, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'code generator', 'prefix': 'a',
        'description': 'Nestled between navigation consoles is a device labeled "Escape Pod Launch Code Generator." It looks like an old-timey vending machine. There\'s a shiny red button and a digital display.',
        'location': 44, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'lockdown console', 'prefix': 'the',
        'description': 'The lockdown console has a small screen that reads: \n\t"LOCKDOWN ENGAGED - Offline systems: Hangar elevator, Deepspace Communications, Escape pods"'
                       '\nThere does not appear to be any way to interact with the console, but there is an empty lever socket just below the screen.',
        'location': 45, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'launch controls', 'prefix': 'the',
        'description': "The launch controls look like a small terminal. There's a screen and a keyboard.",
        'location': 21, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'launch console', 'prefix': 'the',
        'description': "The launch console looks like a small terminal. There's a screen and a keyboard.",
        'location': 22, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'dead crewmate', 'prefix': 'a',
        'description': 'You recognize Petty Officer Smith from your time at the academy. He was always in motion. Now his body lies still. It looks like he suffered several blaster wounds.',
        'location': 32, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'dead engineer', 'prefix': 'a',
        'description': "It's hard to look at the engineer. Her arm is bending the wrong way, and her head was hit hard by something heavy. The damage is so extensive you can't even recognize her.",
        'location': 15, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'retina scanner', 'prefix': 'a',
        'description': 'The scanner is built-into a panel next to the elevator door. '
                       'It sits at about eye-level and sheds a dull red glow.',
        'location': 11, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'phaser booster', 'prefix': 'a',
        'description': 'The booster is a shiny gray widget. In small print it reads, '
                       '"Turns your V-8 into a V-9!"',
        'location': 7, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'medium stimpack', 'prefix': 'a',
        'description': 'The double vials have red hearts etched into their sides. There is only one needle, thankfully.',
        'location': 30, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'clogged toilet', 'prefix': 'a',
        'description': 'The flush mechanism is not responsive. The bowl is stuffed with what looks like a very wet dark blue cloth.',
        'location': 47, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'astroplunger', 'prefix': 'an',
        'description': "Some technology can't be improved upon. "
                       'Despite its fancy name, the wooden handle and dark rubber bulb are fashioned in the classic design.',
        'location': 48, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'workbench', 'prefix': 'the',
        'description': "With this state-of-the-art quantum-precision workbench, "
                       "there's nothing you can't build! The urge to create is almost overwhelming.",
        'location': 49, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'digipad9', 'prefix': 'a',
        'description': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                       "\n\tThey're hunting the custodial staff. I guess it's because we have access to so much of the ship."
                       '\n\tSome of the team is hiding their uniforms. I guess the dark blue color gives us away. -B',
        'location': 6, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'workbench manual', 'prefix': 'a',
        'description': 'You scan the manual for relevant information.'
                       '\n\t...Holding high-heat materials requires gloves reinforced with non-conductive fibers...'
                       '\n\t...A workbench is only as effective as it is clean. Buy our patented Bleakwipes to keep your workspace factory-pure...'
                       '\n\t...Most levers can be constructed with a bar, a grip for holding, and some kind of tip that will connect to...'
                       '\n\t...Fuel cell containers are not worth modifying. StarClunk makes the best...',
        'location': 12, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
]

CREATURES = [
    {
        'id': 0, 'name': 'Prison guard',
        'description': 'The guard is 6 feet tall with a sturdy build, greenish skin, and eyes that are cloudy and dark. Its posture is full of anger. No weapons are visible, but its knuckles look pointy.',
        'room': 1, 'max_hp': 40, 'current_hp': 40, 'is_dead': False, 'is_hostile': False,
        'status_neutral': "It isn't interested in you.", 'status_hostile': "It's very mad at you.",
        'damage': 10, 'hit_bonus': 10, 'attack_chance': 65, 'is_fatigued': False,
        'death_event': 3, 'was_seen': False,
        'dead_description': 'The lifeless body of the prison guard is a foreboding sight.',
    },
    {
        'id': 1, 'name': 'Spry zombie',
        'description': 'This zombified crewmate is short, lithe, and unpredictable. It has that familiar green skin and murky eyes. Blood and bits of flesh are visible on the tips of its fingers.',
        'room': 30, 'max_hp': 60, 'current_hp': 60, 'is_dead': False, 'is_hostile': True,
        'status_neutral': "It isn't interested in you.", 'status_hostile': "It's very mad at you.",
        'damage': 15, 'hit_bonus': 10, 'attack_chance': 70, 'is_fatigued': False,
        'death_event': 12, 'was_seen': False,
        'dead_description': "The zombie looks even smaller now that it's dead.",
    },
    {
        'id': 2, 'name': 'Hulking guard',
        'description': 'This massive guard is a head taller than you, with milky eyes and a ghoulish complexion. Even though its wide body moves slowly, you sense it holds the force of a great catapult within. '
                       'It seems preoccupied, looking all around as it licks its lips and chews its own cheek.',
        'room': 25, 'max_hp': 200, 'current_hp': 200, 'is_dead': False, 'is_hostile': True,
        'status_neutral': "It isn't interested in you.", 'status_hostile': 'It stares hungrily at you.',
        'damage': 20, 'hit_bonus': 5, 'attack_chance': 60, 'is_fatigued': False,
        'death_event': 21, 'was_seen': False,
        'dead_description': "The monstrous heap of wasted flesh is unnerving. You are relieved that it's dead.",
    },
    {
        'id': 3, 'name': 'Captain',
        'description': 'The captain is wearing a spacesuit that offers protection from weapons and the atmosphere. Their helmet has a mirrored visor, but you think you see clear, intense eyes within. '
                       'The captain holds a particle blaster.',
        'room': 43, 'max_hp': 100, 'current_hp': 100, 'is_dead': False, 'is_hostile': False,
        'status_neutral': 'They appear disinterested in you.', 'status_hostile': 'They take aim at you.',
        'damage': 15, 'hit_bonus': 10, 'attack_chance': 70, 'is_fatigued': False,
        'death_event': 31, 'was_seen': False,
        'dead_description': "The captain's spacesuit is badly damaged from the fight, but it isn't moving.",
    },
]

# Event index == event ID.
# Original had two out-of-order insert pairs: (3 before 2) and (12 before 11).
# Python's out-of-bounds insert appends, so the final order was always correct.
# Listed here in the resolved order.
EVENTS = [
    {   # 0 - Swing food tray (weapon flavor text)
        'id': 0, 'done': False, 'room': 999, 'item_name': 'food tray',
        'first_time_text': 'You swing the food tray.',
        'already_done_text': 'You swing the food tray.',
    },
    {   # 1 - Use stimpack: heal +30, leave empty stimpack
        'id': 1, 'done': False, 'room': 999, 'item_name': 'stimpack',
        'first_time_text': 'You jab the stimpack into your thigh. Heat rushes through your body, and you feel better.',
        'already_done_text': 'The stimpack is used up.',
    },
    {   # 2 - Keycard on detention elevator: unlock Main Deck
        'id': 2, 'done': False, 'room': 4, 'item_name': 'keycard',
        'first_time_text': 'The keycard fits nicely into the elevator console. You can now use the elevator!',
        'already_done_text': 'This elevator is already accessible.',
    },
    {   # 3 - Keycard drops from prison guard on death (death_event)
        'id': 3, 'done': False, 'room': 999, 'item_name': 'keycard',
        'first_time_text': 'As the guard falls to the floor, a keycard falls from its pocket.',
        'already_done_text': 'Judging by its markings, this seems like it would be useful at the Detention Elevator Bay.',
    },
    {   # 4 - Use breathing mask: toggle on_person (done never set True — always callable)
        'id': 4, 'done': False, 'room': 999, 'item_name': 'breathing mask',
        'first_time_text': 'The mask fits snugly on your face.',
        'already_done_text': 'The mask fits snugly on your face.',
    },
    {   # 5 - Read digipad1
        'id': 5, 'done': False, 'room': 999, 'item_name': 'digipad1',
        'first_time_text': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                           '\n\tAfter we were attacked, I dragged you in here and set the door to lock from the inside.'
                           '\n\tYou can get out but be careful: most of the crew is dead. Those that survived are, well, dangerous.'
                           '\n\tUse whatever you can to survive. You gotta get off this ship. -B',
        'already_done_text': 'The digipad reads:'
                             '\n\tAfter we were attacked, I dragged you in here and set the door to lock from the inside.'
                             '\n\tYou can get out but be careful: most of the crew is dead. Those that survived are, well, dangerous.'
                             '\n\tUse whatever you can to survive. You gotta get off this ship. -B',
    },
    {   # 6 - Read digipad2
        'id': 6, 'done': False, 'room': 999, 'item_name': 'digipad2',
        'first_time_text': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                           "\n\tSome kind of virus swept through the ship. It killed most of the crew. Others were corrupted."
                           "\n\tThey do not need oxygen. They are diverting the ship's oxygen for some other purpose."
                           '\n\tI locked the atmosphere settings on the Detention Level, but other places on the ship are probably bad. -B',
        'already_done_text': 'The digipad reads:'
                             "\n\tSome kind of virus swept through the ship. It killed most of the crew. Others were corrupted."
                             "\n\tThey do not need oxygen. They are diverting the ship's oxygen for some other purpose."
                             '\n\tI locked the atmosphere settings on the Detention Level, but other places on the ship are probably bad. -B',
    },
    {   # 7 - Swing wrench (weapon flavor text)
        'id': 7, 'done': False, 'room': 999, 'item_name': 'wrench',
        'first_time_text': 'You heave the wrench in a fearsome arc.',
        'already_done_text': 'You heave the wrench in a fearsome arc.',
    },
    {   # 8 - Fuel cell on corpse (room 10): dissolve corpse, drop quarters keycard
        'id': 8, 'done': False, 'room': 10, 'item_name': 'fuel cell',
        'first_time_text': 'You pour the fuel cell onto the petrified corpse. The fuel melts through the green substance, producing a steamy sizzle. It also melts through the clothes and flesh. The stench is vile. '
                           'After a few seconds of that horrific chemical reaction, all that remains in the puddle are a few metal fillings, a useless belt buckle, and a keycard.',
        'already_done_text': 'The fuel cell is used up.',
    },
    {   # 9 - Quarters keycard on elevator (room 13): unlock Crew Quarters
        'id': 9, 'done': False, 'room': 13, 'item_name': 'quarters keycard',
        'first_time_text': 'The keycard fits nicely into the elevator console. You can now use the elevator!',
        'already_done_text': 'This elevator is already accessible.',
    },
    {   # 10 - Read digipad5
        'id': 10, 'done': False, 'room': 999, 'item_name': 'digipad5',
        'first_time_text': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                           "\n\tThe virus doesn't act the same on everybody. It doesn't make sense."
                           '\n\tI saw Jackson from Combat Services collapse. Once she did, a jade-green crystallized coating formed over her skin.'
                           '\n\tOthers went into zombie mode and started attacking. -A',
        'already_done_text': 'The digipad reads:'
                             "\n\tThe virus doesn't act the same on everybody. It doesn't make sense."
                             '\n\tI saw Jackson from Combat Services collapse. Once she did, a jade crystal coating formed over her skin.'
                             '\n\tOthers went into zombie mode and started attacking. -A',
    },
    {   # 11 - Mess keycard on elevator (room 34): unlock Mess & Medical
        'id': 11, 'done': False, 'room': 34, 'item_name': 'mess keycard',
        'first_time_text': 'The keycard fits nicely into the elevator console. You can now use the elevator!',
        'already_done_text': 'This elevator is already accessible.',
    },
    {   # 12 - Mess keycard drops from Spry zombie on death (death_event)
        'id': 12, 'done': False, 'room': 999, 'item_name': 'mess keycard',
        'first_time_text': 'As the zombie falls to the floor, a keycard falls from its pocket.',
        'already_done_text': "Judging by its markings, this seems like it would be useful at the Mess & Medical Elevator Bay.",
    },
    {   # 13 - Scalpel on fallen soldier (room 39): extract soldier eye
        'id': 13, 'done': False, 'room': 39, 'item_name': 'scalpel',
        'first_time_text': 'After gathering resolve, you gently cut an eye out of the fallen soldier and slide it in your pocket. Yuck.',
        'already_done_text': "Haven't you butchered enough already?",
    },
    {   # 14 - Slice with scalpel (weapon flavor text)
        'id': 14, 'done': False, 'room': 999, 'item_name': 'scalpel',
        'first_time_text': 'You slice with the scalpel.',
        'already_done_text': 'You slice with the scalpel.',
    },
    {   # 15 - Use large stimpack: heal +90, leave empty large stimpack
        'id': 15, 'done': False, 'room': 999, 'item_name': 'large stimpack',
        'first_time_text': 'You jab the large stimpack into your thigh. Intense heat surges into your body, and you feel much, much better.',
        'already_done_text': 'The large stimpack is used up.',
    },
    {   # 16 - Read digipad4
        'id': 16, 'done': False, 'room': 999, 'item_name': 'digipad4',
        'first_time_text': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                           "\n\tThey say you can see it in the eyes when they're infected. They get all hazy."
                           "\n\tIf that's true, then it's happening to me. I can't see my own reflection any more. -L",
        'already_done_text': 'The digipad reads:'
                             "\n\tThey say you can see it in the eyes when they're infected. They get all hazy."
                             "\n\tIf that's true, then it's happening to me. I can't see my own reflection any more. -L",
    },
    {   # 17 - Soldier eye on retina scanner (room 11): unlock Armory elevator
        'id': 17, 'done': False, 'room': 11, 'item_name': 'soldier eye',
        'first_time_text': 'You hold the clammy eyeball up to the retina scanner. After repositioning it, the control panel beeps twice '
                           'and displays, "ARMORY ACCESS GRANTED." You can now use the elevator!',
        'already_done_text': 'This elevator is already accessible.',
    },
    {   # 18 - Use soldier eye anywhere else
        'id': 18, 'done': False, 'room': 999, 'item_name': 'soldier eye',
        'first_time_text': "You carefully pull the eye out of your pocket. There doesn't seem to be anything to do with it here. You gladly put it away.",
        'already_done_text': "You're reluctant to remove the eye from your pocket. It's slimy and feels like it is always looking at you.",
    },
    {   # 19 - Read digipad3
        'id': 19, 'done': False, 'room': 999, 'item_name': 'digipad3',
        'first_time_text': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                           '\n\tTraining today in Systems Control. Learned how to activate locked down systems.'
                           '\n\tThey got some real Rube Goldberg protocols. The lever that works the controls is'
                           '\n\tassembled from three parts in storage on the ship. How is that secure? -M',
        'already_done_text': 'The digipad reads:'
                             '\n\tTraining today in Systems Control. Learned how to activate locked down systems.'
                             '\n\tThey got some real Rube Goldberg protocols. The lever that works the controls is'
                             '\n\tassembled from three parts in storage on the ship. How is that secure? -M',
    },
    {   # 20 - Bridge keycard on elevator (room 33): unlock Bridge
        'id': 20, 'done': False, 'room': 33, 'item_name': 'bridge keycard',
        'first_time_text': 'The keycard fits nicely into the elevator console. You can now use the elevator!',
        'already_done_text': 'This elevator is already accessible.',
    },
    {   # 21 - Bridge keycard drops from Hulking guard on death (death_event)
        'id': 21, 'done': False, 'room': 999, 'item_name': 'bridge keycard',
        'first_time_text': 'When the huge guard slumps to the floor, you notice it was holding a keycard in one of its clenched fists.',
        'already_done_text': "The keycard's markings indicate it could be used to access the Bridge elevator.",
    },
    {   # 22 - Fire phaser (weapon flavor text)
        'id': 22, 'done': False, 'room': 999, 'item_name': 'phaser',
        'first_time_text': 'You fire the phaser.',
        'already_done_text': 'You fire the phaser.',
    },
    {   # 23 - Use wound salve: heal +35, leave used jar
        'id': 23, 'done': False, 'room': 999, 'item_name': 'wound salve',
        'first_time_text': 'You apply the salve to your most painful wounds. A cool tingling pulls the ache from your body. You feel better.',
        'already_done_text': 'The wound salve is used up.',
    },
    {   # 24 - Hot sauce on Hulking guard: -25% HP (requires creature in same room)
        'id': 24, 'done': False, 'room': 999, 'item_name': 'hot sauce',
        'first_time_text': "You hurl the bottle at the Hulking guard. It shatters and its contents splatter across the brute's chest and neck. It stumbles, looking diminished by the spicy assault.",
        'already_done_text': 'The hot sauce is gone.',
    },
    {   # 25 - Mayonnaise on Hulking guard: -25% HP (requires creature in same room)
        'id': 25, 'done': False, 'room': 999, 'item_name': 'mayonnaise',
        'first_time_text': 'You chuck the mayo jar at the Hulking guard. Bullseye! It breaks on its forehead, covering its face with cream-covered glass shards. That was a humiliating blow, even for a zombie.',
        'already_done_text': 'The mayonnaise is gone.',
    },
    {   # 26 - Pear powder on Hulking guard: -25% HP (requires creature in same room)
        'id': 26, 'done': False, 'room': 999, 'item_name': 'pear powder',
        'first_time_text': 'You dump the bag of pear powder on the Hulking guard. The yellow crystals stick to its flesh and clothes. The zombie recoils in self-disgust, weakened by the indignity.',
        'already_done_text': 'The pear powder is gone.',
    },
    {   # 27 - Read digipad8
        'id': 27, 'done': False, 'room': 999, 'item_name': 'digipad8',
        'first_time_text': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                           '\n\tThose infected, zombies, whatever--they do not stop.'
                           "\n\tMe and Barb iced 6 of them in the mess hall. Don't know why but food made them real mad."
                           '\n\tIt hurt them too. Hope somebody sees this. -X',
        'already_done_text': 'The digipad reads:'
                             '\n\tThose infected, zombies, whatever--they do not stop.'
                             "\n\tMe and Barb held off 6 of them in the mess hall. Don't know why but food seemed to make them weak."
                             '\n\tOr maybe it just distracted them. Hope somebody sees this. -X',
    },
    {   # 28 - Allen claw on workbench (room 49): assemble override lever if all 3 parts present
        'id': 28, 'done': False, 'room': 49, 'item_name': 'allen claw',
        'first_time_text': 'When you lay your items on the workbench, you see what to do. The allen claw, smooth bar, and gummy grip fit together with a satisfying snap. '
                           "You've made the override lever!",
        'already_done_text': 'Nothing happens.',
    },
    {   # 29 - Smooth bar on workbench (room 49): assemble override lever if all 3 parts present
        'id': 29, 'done': False, 'room': 49, 'item_name': 'smooth bar',
        'first_time_text': 'When you lay your items on the workbench, you see what to do. The allen claw, smooth bar, and gummy grip fit together with a satisfying snap. '
                           "You've made the override lever!",
        'already_done_text': 'Nothing happens.',
    },
    {   # 30 - Gummy grip on workbench (room 49): assemble override lever if all 3 parts present
        'id': 30, 'done': False, 'room': 49, 'item_name': 'gummy grip',
        'first_time_text': 'When you lay your items on the workbench, you see what to do. The allen claw, smooth bar, and gummy grip fit together with a satisfying snap. '
                           "You've made the override lever!",
        'already_done_text': 'Nothing happens.',
    },
    {   # 31 - Captain dies: open bridge door (death_event)
        'id': 31, 'done': False, 'room': 999, 'item_name': 'bridge door',
        'first_time_text': 'After the captain stops twitching, the spacesuit emits a series of beeps. Then the bridge door panel lights up. A second later, the door to the bridge slides open.',
        'already_done_text': 'The door to the bridge is already open.',
    },
    {   # 32 - Use code generator (room 44): generate random launch code
        'id': 32, 'done': False, 'room': 44, 'item_name': 'code generator',
        'first_time_text': 'You press the red button. Random numbers and letters appear quickly then change on the screen. It eventually stops on a short string of characters.',
        'already_done_text': 'You press the button again, but nothing happens. Must be a one-time thing.',
    },
    {   # 33 - Override lever on lockdown console (room 45): lift lockdown, unlock Hangar elevator
        'id': 33, 'done': False, 'room': 45, 'item_name': 'override lever',
        'first_time_text': 'The lever fits nicely into the socket. You pull it down and hear distant machinery grind into action. '
                           'The lockdown console now reads:\n\t"NO LOCKDOWN - Offline systems: none',
        'already_done_text': 'Re-inserting the lever and moving it around has no visible effect on the data displayed.',
    },
    {   # 34 - Use launch controls (room 21): prompt for launch code
        'id': 34, 'done': False, 'room': 21, 'item_name': 'launch controls',
        'first_time_text': 'You activate the launch controls.',
        'already_done_text': 'You activate the launch controls.',
    },
    {   # 35 - Use launch console (room 22): prompt for launch code
        'id': 35, 'done': False, 'room': 22, 'item_name': 'launch console',
        'first_time_text': 'You activate the launch console.',
        'already_done_text': 'You activate the launch console.',
    },
    {   # 36 - Use lockbox: flavor text (no key exists)
        'id': 36, 'done': False, 'room': 999, 'item_name': 'lockbox',
        'first_time_text': "You try prying the box open, but it's locked. The square keyhole is tiny and shallow. It must require an oddly shaped key.",
        'already_done_text': "Still at it? The box is locked. Maybe those symbols mean something?",
    },
    {   # 37 - Use dented tricorder: flavor text
        'id': 37, 'done': False, 'room': 999, 'item_name': 'dented tricorder',
        'first_time_text': "You scan your surroundings, but all the tricorder does is let out two beeps.",
        'already_done_text': 'Scanning...beep...beep.',
    },
    {   # 38 - Use retina scanner without eye (room 11): flavor text; reset when armory unlocked
        'id': 38, 'done': False, 'room': 11, 'item_name': 'retina scanner',
        'first_time_text': 'You peer into the retina scanner. It lets out a low, disapproving beep.',
        'already_done_text': 'You move your head so your other eye is scanned. Still nothing.',
    },
    {   # 39 - Phaser booster on phaser: upgrade weapon (done never set True — always callable)
        'id': 39, 'done': False, 'room': 999, 'item_name': 'phaser booster',
        'first_time_text': "The booster slides nicely onto the phaser. Now you're playing with power.",
        'already_done_text': 'The phaser is already enhanced with the booster.',
    },
    {   # 40 - Use medium stimpack: heal +60, leave empty medium stimpack
        'id': 40, 'done': False, 'room': 999, 'item_name': 'medium stimpack',
        'first_time_text': 'You stick the medium stimpack into your belly. A warm glow courses from your midsection to your extremities. You feel much better.',
        'already_done_text': 'The medium stimpack is used up.',
    },
    {   # 41 - Use clogged toilet (no plunger): flavor text
        'id': 41, 'done': False, 'room': 47, 'item_name': 'clogged toilet',
        "first_time_text": "It doesn't flush, and with all that clothing stuck inside, it seems like a bad idea to use it as designed.",
        "already_done_text": "It doesn't flush, and with all that clothing stuck inside, it seems like a bad idea to use it as designed.",
    },
    {   # 42 - Astroplunger on clogged toilet (room 47): unclog, reveal metal key
        'id': 42, 'done': False, 'room': 47, 'item_name': 'astroplunger',
        'first_time_text': 'You apply your best plunging technique to the clogged toilet. After a vigorous effort, the you extract a drenched custodial uniform! '
                           'The waste purification solution is causing it to quickly dissolve, but a key on a ring that was attached to the uniform belt remains.',
        'already_done_text': "There isn't anything to plunge here.",
    },
    {   # 43 - Metal key on workroom door (room 48): unlock Workroom
        'id': 43, 'done': False, 'room': 48, 'item_name': 'metal key',
        'first_time_text': 'With a little effort, you are able to unlock the door to the Workroom.',
        'already_done_text': 'The workroom door is already unlocked.',
    },
    {   # 44 - Use workbench alone (room 49): flavor text nudge
        'id': 44, 'done': False, 'room': 49, 'item_name': 'workbench',
        'first_time_text': "The workbench by itself doesn't do much. Try experimenting with other items. Did you read the directions?",
        'already_done_text': "It still doesn't do anything. There has to be instructions for this thing.",
    },
    {   # 45 - Read digipad9
        'id': 45, 'done': False, 'room': 999, 'item_name': 'digipad9',
        'first_time_text': "Like other digipads you've seen, this one contains messages sent by your crewmates."
                           "\n\tThey're hunting the custodial staff. I guess it's because we have access to so much of the ship."
                           '\n\tSome of the team is hiding their uniforms. I guess the dark blue color gives us away. -B',
        'already_done_text': 'The digipad reads:'
                             "\n\tThey're hunting the custodial staff. I guess it's because we have access to so much of the ship."
                             '\n\tSome of the team is hiding their uniforms. I guess the dark blue color gives us away. -B',
    },
    {   # 46 - Read workbench manual
        'id': 46, 'done': False, 'room': 999, 'item_name': 'workbench manual',
        'first_time_text': 'You thumb through the manual.'
                           '\n\t...Holding high-heat materials requires gloves reinforced with non-conductive fibers...'
                           '\n\t...A workbench is only as effective as it is clean. Buy our patented Bleakwipes to keep your workspace factory-pure...'
                           '\n\t...Most levers can be constructed with a bar, a grip for holding, and some kind of tip that will connect to...'
                           '\n\t...Fuel cell containers are not worth modifying. StarClunk makes the best...',
        'already_done_text': 'You scan the manual again.'
                             '\n\t...Holding high-heat materials requires gloves reinforced with non-conductive fibers...'
                             '\n\t...Most levers can be constructed with a bar, a grip for holding, and some kind of tip that will connect to...'
                             '\n\t...A workbench is only as effective as it is clean. Buy our patented Bleakwipes to keep your workspace factory-pure...'
                             '\n\t...Fuel cell containers are not worth modifying. StarClunk makes the best...',
    },
]


def _code_checker(state):
    """Prompt for launch code; set state.room to EXIT_ROOM on correct entry."""
    entered_code = input('Enter launch code: ')
    if state.room == 22 and entered_code.lower() == state.launch_code.lower():
        print('The console beeps happily. The screen reads: "LAUNCH SEQUENCE INITIATED"')
        state.room = EXIT_ROOM
    else:
        print('The screen replies: INVALID LAUNCH CODE')


def handle_event(event_id, current_room, state):
    """Execute the side effects for the given event id.

    Reads and writes: state.things, state.world, state.events, state.player_hp,
                      state.launch_code, state.room, state.creatures.
    Calls: state.delete_thing(name), state.add_thing(item_dict).
    Both are wired up in step 2 (GameState).
    """
    event = state.events[event_id]

    # --- Simple events: print text and mark done ---
    if event_id in [0, 5, 6, 7, 10, 14, 16, 18, 19, 22, 27, 36, 37, 38, 41, 44, 45, 46]:
        print(event['first_time_text'])
        event['done'] = True

    # --- Use stimpack: heal +30, leave empty stimpack ---
    elif event_id == 1:
        print(event['first_time_text'])
        event['done'] = True
        state.player_hp = min(state.player_hp + 30, 100)
        state.add_thing({
            'name': 'empty stimpack', 'prefix': 'an',
            'description': 'The hollow tube of the used stimpack is of little use now.',
            'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('stimpack')

    # --- Keycard on detention elevator: unlock Main Deck ---
    elif event_id == 2:
        print(event['first_time_text'])
        event['done'] = True
        state.world[5]['visible'] = True
        state.world[4]['desc'] = 'The elevator goes up to the Main Deck. The detention hallway is to the east.'
        state.world[4]['exits'] = {'e': 1, 'u': 5}
        state.delete_thing('keycard')

    # --- Keycard drops from prison guard on death ---
    elif event_id == 3:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'keycard', 'prefix': 'a',
            'description': 'This sleek card reads, "Detention Elevator." Emblazoned under the text is an image of a box with an arrow inside it.',
            'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })

    # --- Use breathing mask: move to on_person (done never set True) ---
    elif event_id == 4:
        print(event['first_time_text'])
        for thing in state.things:
            if thing['name'].lower() == 'breathing mask':
                if thing['on_person']:
                    return
                thing['on_person'] = True
                state.inventory_quantity += 1

    # --- Fuel cell on corpse: dissolve, drop quarters keycard ---
    elif event_id == 8:
        print(event['first_time_text'])
        event['done'] = True
        state.delete_thing('fuel cell')
        state.delete_thing('corpse')
        state.add_thing({
            'name': 'empty fuel cell', 'prefix': 'an',
            'description': 'The spent fuel cell has nothing inside it.',
            'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })
        state.things.append({
            'name': 'quarters keycard', 'prefix': 'a',
            'description': "After wiping it clean, you see this keycard has the words 'Crew Quarters' printed on it.",
            'location': 10, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })

    # --- Quarters keycard on elevator: unlock Crew Quarters ---
    elif event_id == 9:
        print(event['first_time_text'])
        event['done'] = True
        state.world[28]['visible'] = True
        state.world[13]['desc'] = 'The elevator goes down to Crew Quarters. To the east is a widening hallway.'
        state.world[13]['exits'] = {'e': 12, 'd': 28}
        state.delete_thing('quarters keycard')

    # --- Mess keycard on elevator: unlock Mess & Medical ---
    elif event_id == 11:
        print(event['first_time_text'])
        event['done'] = True
        state.world[35]['visible'] = True
        state.world[34]['desc'] = 'This elevator goes down to the Mess Hall and Medical Services Deck. The observation deck is to the north.'
        state.world[34]['exits'] = {'d': 35, 'n': 32}
        state.delete_thing('mess keycard')

    # --- Mess keycard drops from Spry zombie on death ---
    elif event_id == 12:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'mess keycard', 'prefix': 'a',
            'description': 'This worn card reads, "Mess & Medical Elevator." Emblazoned under the text is an image of a box with an arrow inside it.',
            'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })

    # --- Scalpel on fallen soldier: extract soldier eye ---
    elif event_id == 13:
        print(event['first_time_text'])
        event['done'] = True
        state.add_thing({
            'name': 'soldier eye', 'prefix': 'a',
            'description': "You don't feel great about how you got it, but the eyeball is pretty cool.",
            'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('fallen soldier')
        state.things.append({
            'name': 'fallen soldier', 'prefix': 'a',
            'description': 'This dead crewmate is bent backwards, leaning on the countertop. They have the insignia and fatigues of a tactical combat specialist. '
                           'Unlike the other bodies you encountered, this one seems frozen in shock, face up with one eye and mouth wide open.',
            'location': 39, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
        })

    # --- Use large stimpack: heal +90, leave empty ---
    elif event_id == 15:
        print(event['first_time_text'])
        event['done'] = True
        state.player_hp = min(state.player_hp + 90, 100)
        state.add_thing({
            'name': 'empty large stimpack', 'prefix': 'an',
            'description': "There's not much to do with the large stimpack now that it is drained.",
            'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('large stimpack')

    # --- Soldier eye on retina scanner: unlock Armory elevator ---
    elif event_id == 17:
        print(event['first_time_text'])
        event['done'] = True
        state.world[23]['visible'] = True
        state.world[11]['desc'] = 'The elevator goes down to the Armory. The wide hallway is to the north.'
        state.world[11]['exits'] = {'n': 10, 'd': 23}
        state.events[38]['done'] = False

    # --- Bridge keycard on elevator: unlock Bridge ---
    elif event_id == 20:
        print(event['first_time_text'])
        event['done'] = True
        state.world[42]['visible'] = True
        state.world[33]['desc'] = 'The elevator goes up to the Bridge. To the south is the observation deck.'
        state.world[33]['exits'] = {'s': 32, 'u': 42}
        state.delete_thing('bridge keycard')

    # --- Bridge keycard drops from Hulking guard on death ---
    elif event_id == 21:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'bridge keycard', 'prefix': 'a',
            'description': 'This dark gray card has no words on it, but when held at a certain angle, a stylized bridge materialzes. Below the bridge image you can see a box with an arrow inside it.',
            'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })

    # --- Use wound salve: heal +35, leave used jar ---
    elif event_id == 23:
        print(event['first_time_text'])
        event['done'] = True
        state.player_hp = min(state.player_hp + 35, 100)
        state.add_thing({
            'name': 'used wound salve', 'prefix': 'a',
            'description': 'The wound salve jar is empty. What a shame.',
            'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('wound salve')

    # --- Food items on Hulking guard: reduce HP by 25% each ---
    elif event_id in [24, 25, 26]:
        item_names = {24: 'hot sauce', 25: 'mayonnaise', 26: 'pear powder'}
        if any(c['id'] == 2 and c['room'] == current_room and not c['is_dead'] for c in state.creatures):
            print(event['first_time_text'])
            event['done'] = True
            state.creatures[2]['current_hp'] = int(state.creatures[2]['current_hp'] * 0.75)
            state.delete_thing(item_names[event_id])
        else:
            print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')

    # --- Workbench lever assembly: need all 3 parts in room or on person ---
    elif event_id in [28, 29, 30]:
        parts_present = sum(
            1 for t in state.things
            if t['name'] in ('allen claw', 'smooth bar', 'gummy grip')
            and (t['location'] == current_room or t['on_person'])
        )
        if parts_present == 3:
            state.things.append({
                'name': 'override lever', 'prefix': 'the',
                'description': 'This majestic implement is full of potential. A genuine lever of power.',
                'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
            })
            state.delete_thing('allen claw')
            state.delete_thing('smooth bar')
            state.delete_thing('gummy grip')
            print(event['first_time_text'])
        else:
            print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')

    # --- Captain dies: open bridge door ---
    elif event_id == 31:
        print(event['first_time_text'])
        event['done'] = True
        state.world[44]['visible'] = True
        state.world[43]['desc'] = 'This is the bridge-level security desk. An open door to the bridge is to the west. To the east is the Systems Control room. South is an elevator bay.'
        state.world[43]['exits'] = {'w': 44, 'e': 45, 's': 42}

    # --- Code generator: generate random launch code ---
    elif event_id == 32:
        print(event['first_time_text'])
        event['done'] = True
        state.launch_code = (
            str(random.randrange(0, 10)) + str(random.randrange(0, 10))
            + 'L07A'
            + str(random.randrange(0, 10)) + str(random.randrange(0, 10))
        )
        print('It reads: ' + state.launch_code)

    # --- Override lever on lockdown console: lift lockdown, activate Hangar elevator ---
    elif event_id == 33:
        print(event['first_time_text'])
        event['done'] = True
        state.world[19]['visible'] = True
        state.world[9]['desc'] = 'The elevator goes down to the Hangar. To the south is the walkway.'
        state.world[9]['exits'] = {'s': 8, 'd': 19}
        state.delete_thing('lockdown console')
        state.things.append({
            'name': 'lockdown console', 'prefix': 'the',
            'description': 'The lockdown console has a small screen that reads: \n\t"NO LOCKDOWN - Offline systems: none"'
                           '\nThere is an empty lever socket just below the screen.',
            'location': 45, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
        })

    # --- Launch controls / launch console: prompt for code (done never set True) ---
    elif event_id in [34, 35]:
        print(event['first_time_text'])
        _code_checker(state)

    # --- Phaser booster: upgrade phaser (done never set True) ---
    elif event_id == 39:
        print(event['first_time_text'])
        state.delete_thing('phaser')
        state.delete_thing('phaser booster')
        state.add_thing({
            'name': 'phaser', 'prefix': 'a',
            'description': 'The V-8 phaser pistol is a reliable mid- to close-range weapon, especially now that it is BOOSTED.',
            'location': current_room, 'on_person': True, 'moveable': True,
            'is_weapon': True, 'base_damage': 25, 'damage': 30, 'hit_bonus': 45, 'no_drop': False,
        })

    # --- Use medium stimpack: heal +60, leave empty ---
    elif event_id == 40:
        print(event['first_time_text'])
        event['done'] = True
        state.player_hp = min(state.player_hp + 60, 100)
        state.add_thing({
            'name': 'empty medium stimpack', 'prefix': 'an',
            'description': 'The medium stimpack served its purpose.',
            'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('medium stimpack')

    # --- Astroplunger on clogged toilet: extract metal key ---
    elif event_id == 42:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'metal key', 'prefix': 'a',
            'description': 'This small, silvery key has all the notches and grooves you expect to see in something that could unlock a door.',
            'location': 47, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('clogged toilet')
        state.things.append({
            'name': 'toilet', 'prefix': 'a',
            'description': "The flush mechanism still doesn't work, but at least it is empty.",
            'location': 47, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
        })

    # --- Metal key on workroom door: unlock Workroom ---
    elif event_id == 43:
        print(event['first_time_text'])
        event['done'] = True
        state.world[49]['visible'] = True
        state.world[48]['desc'] = 'This dingy space contains an array of maintenance tools and equipment. To the northeast is the Funneling hallway. On the west side of the room is a door to the Workroom. '
        state.world[48]['exits'] = {'ne': 12, 'w': 49}


def handle_special(current_room, state):
    """Bad-air damage outside Detention Level; captain monologue at room 43."""
    if current_room >= 5:
        for thing in state.things:
            if thing['name'].lower() == 'breathing mask':
                if not thing['on_person']:
                    print('The air is too thin to breathe. You feel your lungs shriveling.')
                    state.player_hp -= 30
                    player_wellness(state)

    if current_room == 43 and not state.creatures[3]['is_dead']:
        if not state.creatures[3]['is_hostile'] and not state.special_done[0]['done']:
            print(
                'The ship\'s captain is standing in the middle of the room. They speak to you in a haughty tone:'
                '\n\t"So you survived. I had to bring the virus on board to see if it was effective. It was, even against a crew that fought back.'
                '\n\tWe will learn much from our discovery. No one needs to know about our role in this."\n'
            )
            state.special_done[0]['done'] = True
        elif state.creatures[3]['is_hostile'] and not state.special_done[1]['done']:
            print(
                '\nWith disdain, the captain utters:'
                '\n\t"If you aren\'t willing to go along, you must be silenced. What\'s one more among the dead? '
                '\n\tYou will never make it off my ship!"\n'
            )
            state.special_done[1]['done'] = True
