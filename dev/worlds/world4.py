"""
World 4 — Lake Tortuga

Data: room definitions, items, events, creatures (ROOMS, ITEMS, EVENTS, CREATURES).
Logic: handle_event() for all world-4-specific event side effects,
       including the turtle transformation, multi-step clam-shell unlock,
       and creature-release events.

Replaces the choice == '4' block inside load_game(), do_event(),
do_multi_step_event(), and do_special() in games.py.
"""

import random

STARTING_ROOM = 0
EXIT_ROOM = 2
SAFE_ROOMS = [11, 30, 31, 32, 33]
SPECIAL_ROOMS = [12] + list(range(13, 34))
SPECIAL_DONE = [{'id': 0, 'done': False}]

INTRO_TEXT = (
    '*** Welcome to Lake Tortuga ***\n\n'
    "You just got home from school. It was a long day. You aren't tired, but you feel a little uneasy. "
    "Maybe it's the note that someone stuffed in your pocket while you were riding the bus. "
    "As you grab for the note, you hear a voice.\n\n"
    "\t'Reveal the note to find your way.'\n\n"
    'Startled, you drop the note onto the floor.\n'
)

OUTRO_TEXT = (
    'You are back at home.\n'
    'Your heroism has restored the ecosystem of Lake Tortuga. All creatures, especially the turtles, rejoice.\n\n'
    "You've won the game! Thanks for playing."
)

ROOMS = [
    {   # 0 - Foyer
        'visible': True, 'name': 'Foyer', 'prefix': 'in the', 'name2': '',
        'desc': 'This entryway is just inside the front door of your home. Most of the house is accessible from here. The dining room lies to the west, the living room is south, a stairway leads up to the second-level rooms, '
                'and a door to the garage is east. On the northern wall is the front door, but some force is keeping it shut.',
        'exits': {'s': 4, 'w': 1, 'e': 5, 'u': 6},
    },
    {   # 1 - Dining room
        'visible': True, 'name': 'Dining room', 'prefix': 'in the', 'name2': '',
        'desc': 'Many happy meals were shared at the table in this room. It connects to the kitchen to the south, and the foyer opens to the east.',
        'exits': {'s': 3, 'e': 0},
    },
    {   # 2 - Home (exit room)
        'visible': True, 'name': 'Home', 'prefix': 'at', 'name2': '',
        'desc': 'It feels good to be home.',
        'exits': {},
    },
    {   # 3 - Kitchen
        'visible': True, 'name': 'Kitchen', 'prefix': 'in the', 'name2': '',
        'desc': 'The décor in the kitchen is dated, but functional. The dining room is to the north.',
        'exits': {'n': 1},
    },
    {   # 4 - Living room
        'visible': True, 'name': 'Living room', 'prefix': 'in the', 'name2': '',
        'desc': 'This inviting space encourages you to lounge on the plush furniture. The foyer is visible to the north',
        'exits': {'n': 0},
    },
    {   # 5 - Garage
        'visible': True, 'name': 'Garage', 'prefix': 'in the', 'name2': '',
        'desc': 'The garage is filled with a musty smell. Tools and spare car parts line the walls. A box of curious junk was spilled across the workbench. The door back into the house is to the west. The door to the outside seems to be jammed.',
        'exits': {'w': 0},
    },
    {   # 6 - Landing
        'visible': True, 'name': 'Landing', 'prefix': 'on the', 'name2': '',
        'desc': "At the top of the stairs is a narrow landing. It leads west to your bedroom, and a door to your parents' room is south. You can see the foyer at the bottom of the stairs.",
        'exits': {'w': 7, 's': 8, 'd': 0},
    },
    {   # 7 - Bedroom
        'visible': True, 'name': 'Bedroom', 'prefix': 'in your', 'name2': '',
        'desc': 'A small but functional desk, a dresser, and an unmade bed take up space in the dim room. The door to the landing is east.',
        'exits': {'e': 6},
    },
    {   # 8 - Parent's bedroom
        'visible': True, 'name': "Parent's bedroom", 'prefix': 'in your', 'name2': '',
        'desc': 'A large bed dominates the space. On the opposing wall, a wide mirror is hung above a squat dresser. The only exit is to the north.',
        'exits': {'n': 6},
    },
    {   # 9 - Street (hidden until front door unlocked)
        'visible': False, 'name': 'Street', 'prefix': 'on the', 'name2': '',
        'desc': 'A few trees line this quiet single-lane road that winds past your home. Your house is directly south. From the north you can hear the water lap at the shore of the lake.',
        'exits': {'s': 0, 'n': 10},
    },
    {   # 10 - Lakeshore
        'visible': True, 'name': 'Lakeshore', 'prefix': 'at the', 'name2': '',
        'desc': 'A rocky, muddy shoreline separates the gently rippling lake water from a path south to the street. To the northeast is a pier that extends into the lake.',
        'exits': {'s': 9, 'ne': 11},
    },
    {   # 11 - Pier
        'visible': True, 'name': 'Pier', 'prefix': 'on the', 'name2': '',
        'desc': 'The splintered planks of the pier jut into the murky lake. Rocks, lily pads, and cattails dot the surrounding waters. Dry land is to the southwest.',
        'exits': {'sw': 10},
    },
    {   # 12 - Surface (hidden until ring of power forged)
        'visible': False, 'name': 'Surface', 'prefix': 'floating on the', 'name2': '',
        'desc': 'The cool lake water ripples past toward the shore. Through the grainy water, you see a small clearing in the water below. The pier looms a few feet above the water.',
        'exits': {'d': 13},
    },
    {   # 13 - South shallows
        'visible': True, 'name': 'South shallows', 'prefix': 'in the', 'name2': '',
        'desc': "As you swim through the water, you see the shallows extend to the east and to the west. A cave network is accessible below. You can see the pier through the water's surface above.",
        'exits': {'e': 14, 'w': 20, 'u': 12, 'd': 21},
    },
    {   # 14 - Southeast shallows
        'visible': True, 'name': 'Southeast shallows', 'prefix': 'in the', 'name2': '',
        'desc': 'You are swimming in shallow water in the southeast corner of the lake. You see clearings to the west and to the north. A large log extends from the sandy bottom up to the surface.',
        'exits': {'w': 13, 'n': 15, 'u': 30},
    },
    {   # 15 - East shallows
        'visible': True, 'name': 'East shallows', 'prefix': 'in the', 'name2': '',
        'desc': 'Swimming through the shallow water, you see clearings to the north and the south. Below you is another entrance to a craggy tunnel.',
        'exits': {'n': 16, 's': 14, 'd': 23},
    },
    {   # 16 - Northeast shallows
        'visible': True, 'name': 'Northeast shallows', 'prefix': 'in the', 'name2': '',
        'desc': 'You are swimming in shallow water in the northeast corner of the lake. Clearings are visible to the south and west. A moss-covered boulder pokes its head out of the water to the surface above.',
        'exits': {'s': 15, 'w': 17, 'u': 31},
    },
    {   # 17 - North shallows (n:36 is a debug exit left in from development)
        'visible': True, 'name': 'North shallows', 'prefix': 'in the', 'name2': '',
        'desc': "Tall reeds are thick in the northern edge of the lake. As you swim through the water, you see the surface above. A giant clam shell rests on the northern edge of this clearing. It is firmly shut. The shallows extend to the east and to the west. Another cave entrance lies below.",
        'exits': {'e': 16, 'w': 18, 'd': 25, 'n': 36},
    },
    {   # 18 - Northwest shallows
        'visible': True, 'name': 'Northwest shallows', 'prefix': 'in the', 'name2': '',
        'desc': "The water in the northwest corner of the lake is choked with silt. Clearings are visible to the south and east. A massive branch from a long-dead tree provides a path up to the water's surface above. You almost miss the tiny alcove to the southeast.",
        'exits': {'s': 19, 'e': 17, 'u': 32, 'se': 42},
    },
    {   # 19 - West shallows
        'visible': True, 'name': 'West shallows', 'prefix': 'in the', 'name2': '',
        'desc': 'As you glide through the shallow water, skirting rocks along the western edge of the lake, you spot clearings to the north and the south. Between a cluster of grim stones below is a narrow opening.',
        'exits': {'n': 18, 's': 20, 'd': 27},
    },
    {   # 20 - Southwest shallows
        'visible': True, 'name': 'Southwest shallows', 'prefix': 'in the', 'name2': '',
        'desc': 'This section of the lake is especially rocky. Even for you, it takes great concentration to navigate the shallow waters. More open areas of the lake are visible to the north and east. Between those exits, you spot an opening in the rocks to the northeast. A tall, slender stone runs from the depths below to a flat area just above you.',
        'exits': {'n': 19, 'e': 13, 'ne': 39, 'u': 33},
    },
    {   # 21 - Southern depths
        'visible': True, 'name': 'Southern depths', 'prefix': 'in the', 'name2': '',
        'desc': 'This narrow entryway is a crossroads of underwater tunnels. The cave winds to the northeast and northwest, and opens to the darkness below. A route up to the shallow water of the lake is visible above.',
        'exits': {'ne': 22, 'nw': 28, 'd': 29, 'u': 13},
    },
    {   # 22 - Southeast tunnel
        'visible': True, 'name': 'Southeast tunnel', 'prefix': 'in the', 'name2': '',
        'desc': 'Jagged rocks make up the walls of this tunnel that runs from the southwest to the northeast. An inflated air bladder juts out from the eastern wall. It completely fills an opening that looks big enough for you to swim through.',
        'exits': {'sw': 21, 'ne': 23},
    },
    {   # 23 - Eastern depths
        'visible': True, 'name': 'Eastern depths', 'prefix': 'in the', 'name2': '',
        'desc': 'It seems like a little room has been carved into the stone, but the weight of the surrounding rocks makes you uneasy. Fortunately, there are exits to the southwest and northwest. A hole in the center of the cavern leads down to an even darker place. Above you see friendly shallow waters.',
        'exits': {'sw': 22, 'nw': 24, 'd': 29, 'u': 15},
    },
    {   # 24 - Northeast tunnel
        'visible': True, 'name': 'Northeast tunnel', 'prefix': 'in the', 'name2': '',
        'desc': 'You cruise through this smooth, wide tunnel that winds from the southeast to the northwest.',
        'exits': {'se': 23, 'nw': 25},
    },
    {   # 25 - Northern depths
        'visible': True, 'name': 'Northern depths', 'prefix': 'in the', 'name2': '',
        'desc': 'A rough, bent path has been cut through this space, leaving openings to the southwest and southeast. Below is an opening into a darker section of the cave network. A shaft of light streams down from above.',
        'exits': {'sw': 26, 'se': 24, 'd': 29, 'u': 17},
    },
    {   # 26 - Northwest tunnel
        'visible': True, 'name': 'Northwest tunnel', 'prefix': 'in the', 'name2': '',
        'desc': 'You find this plain passageway is a little warmer than the surrounding waters. It opens to the northeast and southwest.',
        'exits': {'ne': 25, 'sw': 27},
    },
    {   # 27 - Western depths
        'visible': True, 'name': 'Western depths', 'prefix': 'in the', 'name2': '',
        'desc': 'The water in this space is thick with small debris, making it hard to see. You feel that the cavern bends like an elbow leading to tunnels to the northeast and southeast. Greater darkness and a slight current are pulling you downward. You see the shallow, clearer waters of the lake above you.',
        'exits': {'ne': 26, 'se': 28, 'd': 29, 'u': 19},
    },
    {   # 28 - Southwest tunnel
        'visible': True, 'name': 'Southwest tunnel', 'prefix': 'in the', 'name2': '',
        'desc': 'This cramped passage runs in a northwest-to-southeast direction. To the southwest you see an opening you could swim through.',
        'exits': {'nw': 27, 'se': 21, 'sw': 41},
    },
    {   # 29 - Cave center
        'visible': True, 'name': 'Cave center', 'prefix': 'in the', 'name2': '',
        'desc': 'This circular room feels like the inside of a well. Passageways out are high on the northern, southern, eastern, and western sides of the space. At the bottom is a bulky, round door made of rotted wood. Somehow a darkness seeps through the cracks of the door.',
        'exits': {'n': 25, 's': 21, 'e': 23, 'w': 27, 'd': 34},
    },
    {   # 30 - Sun-blanched log (safe room, surface)
        'visible': True, 'name': 'Sun-blanched log', 'prefix': 'on a', 'name2': '',
        'desc': 'The bark of this wide log is somehow intact. It serves as a comfortable surface when in direct sunlight. You can follow the log back down into the water.',
        'exits': {'d': 14},
    },
    {   # 31 - Warm boulder (safe room, surface)
        'visible': True, 'name': 'Warm boulder', 'prefix': 'on a', 'name2': '',
        'desc': 'The rockface that sticks out of the water is dry and bedded with spongy moss. You can scale the boulder back down into the water.',
        'exits': {'d': 16},
    },
    {   # 32 - Dead branch (safe room, surface)
        'visible': True, 'name': 'Dead branch', 'prefix': 'on a', 'name2': '',
        'desc': 'Several crooks in this partially submerged branch can be nestled into. The leaves are long-gone, leaving the you exposed to the open sky. You can follow the branch back down into the shallow water.',
        'exits': {'d': 18},
    },
    {   # 33 - Stony mini-mesa (safe room, surface)
        'visible': True, 'name': 'Stony mini-mesa', 'prefix': 'on a', 'name2': '',
        'desc': 'This rock outcropping feels like the top of a desert butte, though it is surrounded by water. Just head back down the stone to re-enter the shallow lake.',
        'exits': {'d': 20},
    },
    {   # 34 - Antechamber
        'visible': True, 'name': 'Antechamber', 'prefix': 'in the', 'name2': '',
        'desc': 'Glowing creepy-crawlies provide the only light in this unfriendly pit. The way back to the well is above. A hollow dread pulls at you from the room to the south.',
        'exits': {'u': 29, 's': 35},
    },
    {   # 35 - Slimy core
        'visible': True, 'name': 'Slimy core', 'prefix': 'in the', 'name2': '',
        'desc': 'This wide cavern seems impossibly large. It must extend deep into the earth. Morose stone and decayed roots line the walls. The only exit is to the north. A circular hole has been bored into the eastern wall, near the floor. It is too small get into.',
        'exits': {'n': 34},
    },
    {   # 36 - Mermaid's grotto (hidden until all 3 shell buttons pressed)
        'visible': False, "name": "Mermaid's grotto", 'prefix': 'in the', 'name2': '',
        'desc': 'The low ceiling of this deep recess makes you feel closed-in. Seashells cover the floor. There is a small door to the south.',
        'exits': {'s': 17},
    },
    {   # 37 - Industrial pipe (accessible after air bladder popped)
        'visible': True, 'name': 'Industrial pipe', 'prefix': 'in the', 'name2': '',
        'desc': 'The entire surface of this cylindrical tube is covered in a green substance. If you focus on it, the surface seems to pulsate slowly. There is a grate on the east end, but enough of it has been worn, or eaten, away for you to proceed. The west end of the pipe leads back to the cave.',
        'exits': {'e': 38, 'w': 22},
    },
    {   # 38 - Tank room
        'visible': True, 'name': 'Tank room', 'prefix': 'in the', 'name2': '',
        'desc': 'It seems like you are inside a voluminous, decaying tank. Mechanical filters are choked with dark green mossy fibers. Wispy tendrils undulate from the ceiling and walls. The pipe that brought you into this place is to the west.',
        'exits': {'w': 37},
    },
    {   # 39 - Rocky passage
        'visible': True, 'name': 'Rocky passage', 'prefix': 'in a', 'name2': '',
        'desc': 'This rough-hewn throughway appears to be carved by unnatural forces. It is a T-intersection. You can swim to the north, northeast, and southwest.',
        'exits': {'n': 40, 'ne': 41, 'sw': 20},
    },
    {   # 40 - Murky chamber
        'visible': True, 'name': 'Murky chamber', 'prefix': 'in the', 'name2': '',
        'desc': "A pile of rocks fills a corner of the room, mounting up to the ceiling and possibly beyond. You can't go that way, but a rope extends through the opening. It is connected to a large cage resting on the floor. A gentle current flows through this room, from the south to the east.",
        'exits': {'s': 39, 'e': 41},
    },
    {   # 41 - Twisty tunnel
        'visible': True, 'name': 'Twisty tunnel', 'prefix': 'in a', 'name2': '',
        'desc': 'Something must have carved through the rock to make this jagged path. The ways out are to the west, northeast, and southwest.',
        'exits': {'w': 40, 'ne': 28, 'sw': 39},
    },
    {   # 42 - Curious alcove
        'visible': True, 'name': 'Curious alcove', 'prefix': 'in a', 'name2': '',
        'desc': 'This small room was hollowed out from the nearby rocks. The water is thick with particles, but you see an ancient stone fountain connected to the eastern wall. You can leave the alcove by heading northwest.',
        'exits': {'nw': 18},
    },
    {   # 43 - Nether (unused room; hammer placed here to avoid a claws attack bug)
        'visible': False, 'name': 'Nether', 'prefix': 'in the', 'name2': '',
        'desc': 'You are nowhere.',
        'exits': {},
    },
]

ITEMS = [
    {   # placed in unused Nether room to avoid a claws attack bug
        'name': 'hammer', 'prefix': 'a',
        'description': "It's a classic ball-peen hammer. Could do some real damage.",
        'location': 43, 'on_person': False, 'moveable': True,
        'is_weapon': True, 'base_damage': 10, 'damage': 30, 'hit_bonus': 20, 'no_drop': False,
    },
    {
        'name': 'faded note', 'prefix': 'a',
        'description': "After you smooth out the crumpled note, you see faint writing on the left half of the page. It reads:\n\n"
                       "\t'Our lake has been overtaken by\n"
                       "\t This creature of the sea has\n"
                       "\t Only the one who wears the rin\n"
                       "\t The one who bears symbols of\n"
                       "\t Peril now fills the lake. If y\n"
                       "\t Find the guardians, remove th",
        'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'hex nut', 'prefix': 'a',
        'description': 'This sturdy piece of steel has a threaded hole in the middle. The six-sided shape feels familiar.',
        'location': 5, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'shirt', 'prefix': 'a',
        'description': 'This dark navy T-shirt has an image of the powerful band of heroes, the Teenage Mutant Ninja Turtles.',
        'location': 7, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'kitchen sink', 'prefix': 'the',
        'description': "A few dishes and forks with caked-on egg are all that remain from this morning's breakfast. A gleaming water droplet trembles at the lip of the faucet.",
        'location': 3, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'filter', 'prefix': 'a',
        'description': "The short metallic tube looks like it would fit on a water faucet. There's a faded, turtle-shell pattern covering the filter.",
        'location': 5, 'on_person': False, 'moveable': True,
        'is_weapon': True, 'base_damage': 0, 'damage': 0, 'hit_bonus': 0, 'no_drop': False,
    },
    {
        'name': 'claws', 'prefix': 'your',
        'description': 'Careful with those things. They look pointy!',
        'location': 12, 'on_person': False, 'moveable': True,
        'is_weapon': True, 'base_damage': 10, 'damage': 30, 'hit_bonus': 30, 'no_drop': True,
    },
    {
        'name': 'shell button', 'prefix': 'a',
        'description': 'Sticking out from the wall is an ivory-colored shell. It looks like you could push it.',
        'location': 39, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'snail shell', 'prefix': 'a',
        'description': "The empty snail shell is dark brown in color, blending into the rock it rests on. It can't be picked up, but it seems to have some give when pressed.",
        'location': 15, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'conch', 'prefix': 'a',
        'description': 'The swirling pattern of this conical shell is mesmerizing. It is loosely wedged into the side of the passageway.',
        'location': 26, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'duckweed', 'prefix': 'some',
        'description': 'These bright green water lentils look like they could be a healthy snack.',
        'location': 19, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'lake lettuce', 'prefix': 'some',
        'description': "It's a marvel that such a succulent plant could grow in these murky waters. The leafy mass seems like it could restore your strength.",
        'location': 21, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'water grubs', 'prefix': 'some',
        'description': "If they weren't slimy, hairy, and wriggling, these beetle larvae might be cute. Never mind that--you're more interested in the tasty protein they provide.",
        'location': 24, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'air bladder', 'prefix': 'an',
        'description': "The massive balloon that blocks the way east is made of high-grade industrial rubber. It looks like it could be popped, but your claws aren't sharp enough.",
        'location': 22, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'fountain', 'prefix': 'the',
        'description': "Although you're already in the lake, a jet of pure water springs from this fountain. It cuts through the surrounding filth.",
        'location': 42, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'lobster trap', 'prefix': 'a',
        'description': 'Distressed wood and rusted wire are fashioned into a large cage. Tied to the top is the rope that leads through the opening above. An enormous crayfish with a burnt umber carapace is coiled within the trap. It does not look happy. A worn lock is all that keeps its deadly pincers at bay.',
        'location': 40, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {   # defensive "weapon" — damage values of -999 trigger the shell defense mechanic
        'name': 'shell', 'prefix': 'your',
        'description': 'Your shell is a beautiful dome of protection. Use it for the perfect defense.',
        'location': 12, 'on_person': False, 'moveable': True,
        'is_weapon': True, 'base_damage': -999, 'damage': -999, 'hit_bonus': -999, 'no_drop': True,
    },
    {
        'name': 'remote', 'prefix': 'the',
        'description': 'The remote controller looks like it could operate any of the video and audio devices in the house. Unfortunately, it needs two AA batteries to work.',
        'location': 4, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'batteries', 'prefix': 'the',
        'description': 'The two C batteries look like they have plenty of charge.',
        'location': 5, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'leather boot', 'prefix': 'a',
        'description': "There are no laces in the sodden boot. Its tongue flops around in defeat.",
        'location': 28, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'wild celery', 'prefix': 'the',
        'description': 'Long ribbon-like leaves spiral upward from the bottom of the lake.',
        'location': 14, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
    {
        'name': 'clam shell', 'prefix': 'the',
        'description': "The enormous rigid shell is impenetrable, wih ridges that make you think of giant waves. It's so big that you can't see around it. Some say a clam is nature's zipper.",
        'location': 17, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
    },
]

CREATURES = [
    {
        'id': 0, 'name': 'Mermaid',
        'description': 'The mermaid floats with such grace, it is almost hypnotic. She carries a glorious trident.',
        'room': 36, 'max_hp': 100, 'current_hp': 100, 'is_dead': False, 'is_hostile': False,
        'status_neutral': "She isn't interested in you, but she eyes you warily.", 'status_hostile': "She's very mad at you.",
        'damage': 10, 'hit_bonus': 10, 'attack_chance': 70, 'is_fatigued': False,
        'death_event': 12, 'was_seen': False,
        'dead_description': "The mermaid's lifeless body is elegant even in death.",
    },
    {
        'id': 1, 'name': 'Algae',
        'description': 'The blob of algae pulses slowly. A green-gray pattern swirls across and through its amoeba-like body.',
        'room': 38, 'max_hp': 100, 'current_hp': 100, 'is_dead': False, 'is_hostile': False,
        'status_neutral': 'A menacing energy flows through it.', 'status_hostile': 'It has shifted into an aggressive shape.',
        'damage': 5, 'hit_bonus': 15, 'attack_chance': 65, 'is_fatigued': False,
        'death_event': 14, 'was_seen': False,
        'dead_description': 'Bits of algae hang in the water, an ominous reminder of the potent creature.',
    },
    # Crayfish and Sea serpent are added dynamically via handle_event (events 16 and 19).
]

# Event index == event ID.
# Original had one out-of-order pair: events.insert(12,...) before events.insert(4,...).
# Python's out-of-bounds insert appended 12_dict, then inserts 4-11 shifted it to index 12.
# Final order is correct: listed here in the resolved order.
EVENTS = [
    {   # 0 - Filter on kitchen sink: create enhanced faucet
        'id': 0, 'done': False, 'room': 3, 'item_name': 'filter',
        'first_time_text': "You screw the filter onto the faucet, making a marked improvement. Maybe it's just the light, but it seems to glow slightly.",
        'already_done_text': "It looks perfect where it is. There's nothing more to do with it.",
    },
    {   # 1 - Enhanced faucet (room 3): reveal note text, open front door (needs faded note present)
        'id': 1, 'done': False, 'room': 3, 'item_name': 'enhanced faucet',
        'first_time_text': "A stream of clear light pours from the faucet. You are compelled to put the faded note under the gentle flow, and when you do, letters begin to take shape on the blank part of the page!\n\nFrom the front of the house, you hear a strange 'pop,' or maybe a 'zap?' You didn't notice it before, but the air feels like it is flowing freely again.",
        'already_done_text': 'A soothing stream of water splashes into the sink.',
    },
    {   # 2 - Wear shirt: move to on_person (done never set True — always callable)
        'id': 2, 'done': False, 'room': 999, 'item_name': 'shirt',
        'first_time_text': 'The T-shirt fits perfectly. You feel invincible.',
        'already_done_text': 'The T-shirt fits perfectly. You feel invincible.',
    },
    {   # 3 - Hex nut on pier (room 11): forge ring of power if wearing shirt
        'id': 3, 'done': False, 'room': 11, 'item_name': 'hex nut',
        'first_time_text': "Standing at the water's edge, wearing the Teenage Mutant Ninja Turtles shirt, the hex nut transforms into a ring. This metallic band fits snugly on your right index finger. "
                           "You've made the RING OF POWER! You cannot remove the ring, but with it you can now descend into the lake!",
        'already_done_text': 'Nothing happens.',
    },
    {   # 4 - Trident on air bladder (room 22): pop bladder, reveal Industrial pipe
        'id': 4, 'done': False, 'room': 22, 'item_name': 'trident',
        'first_time_text': 'You jab the pointy end of the trident into the bladder. It pierces the thick material causing air bubbles to rush out and escape towards the surface. As the bladder deflates, you see a round opening to the east!',
        'already_done_text': 'You poke the trident into the air.',
    },
    {   # 5 - Use claws (weapon flavor text)
        'id': 5, 'done': False, 'room': 999, 'item_name': 'claws',
        'first_time_text': 'You slash with your claws.',
        'already_done_text': 'You slash with your claws.',
    },
    {   # 6 - Use shell button (room 39): press first guardian shell
        'id': 6, 'done': False, 'room': 39, 'item_name': 'shell button',
        'first_time_text': 'You push the shell into the wall.',
        'already_done_text': 'The shell is already pressed into the wall.',
    },
    {   # 7 - Use snail shell (room 15): press second guardian shell
        'id': 7, 'done': False, 'room': 15, 'item_name': 'snail shell',
        'first_time_text': 'You push the snail shell into the rock. It is surprisingly sturdy for something that looks delicate.',
        'already_done_text': 'The snail shell is already depressed into the rock.',
    },
    {   # 8 - Use conch (room 26): press third guardian shell
        'id': 8, 'done': False, 'room': 26, 'item_name': 'conch',
        'first_time_text': 'The conch slides deeper into the wall.',
        'already_done_text': "Only the tip of the conch is accessible. You can't push it farther in or remove it.",
    },
    {   # 9 - Eat duckweed: heal 40-60 HP
        'id': 9, 'done': False, 'room': 999, 'item_name': 'duckweed',
        'first_time_text': 'You shove a clawful of duckweed into your mouth. A current of strength flows through your body, and you feel better.',
        'already_done_text': 'The duckweed served its purpose.',
    },
    {   # 10 - Eat lake lettuce: heal 45-65 HP
        'id': 10, 'done': False, 'room': 999, 'item_name': 'lake lettuce',
        'first_time_text': 'The broad leaves of lake lettuce are surprisingly flavorful. With each bite, you feel your aches and wounds fade.',
        'already_done_text': 'The lake lettuce was delicious.',
    },
    {   # 11 - Eat water grubs: heal 50-70 HP
        'id': 11, 'done': False, 'room': 999, 'item_name': 'water grubs',
        'first_time_text': "Those squirmy suckers know what's about to happen. You pop them into your mouth one by one. Each one oozes like a jelly donut as you start munching. It's invigorating.",
        'already_done_text': 'The water grubs were so satisfying.',
    },
    {   # 12 - Trident drops from Mermaid on death (death_event)
        'id': 12, 'done': False, 'room': 999, 'item_name': 'trident',
        'first_time_text': 'As the mermaid becomes still, she drops the fearsome trident.',
        'already_done_text': 'You poke the trident into the air.',
    },
    {   # 13 - Curious blob in fountain (room 42): extract rusty key
        'id': 13, 'done': False, 'room': 42, 'item_name': 'curious blob',
        'first_time_text': 'You hold the blob under the current of clean water flowing from the fountain. The yellowish shape breaks apart, leaving you with a rusty key!',
        'already_done_text': 'It is no longer a blob.',
    },
    {   # 14 - Curious blob drops from Algae on death (death_event)
        'id': 14, 'done': False, 'room': 999, 'item_name': 'curious blob',
        'first_time_text': 'With that final swipe, the algae begins disintegrating. It was concealing a dark yellow blob that hangs suspended in the water. ',
        'already_done_text': "Not sure how you're supposed to use that.",
    },
    {   # 15 - Use fountain (room 42): extract rusty key if curious blob is present
        'id': 15, 'done': False, 'room': 42, 'item_name': 'fountain',
        'first_time_text': 'You hold the blob under the current of clean water flowing from the fountain. The yellowish shape breaks apart, leaving you with a rusty key!',
        'already_done_text': 'You hold your claws under the cleansing stream. Feels nice.',
    },
    {   # 16 - Rusty key on lobster trap (room 40): unlock cage, release Crayfish
        'id': 16, 'done': False, 'room': 40, 'item_name': 'rusty key',
        'first_time_text': 'With some effort, you are able to fit the rusty key into the lock on the cage. You turn the key, and the lock falls apart. The crayfish senses the opportunity and bursts from the trap!',
        'already_done_text': 'The cage is unlocked.',
    },
    {   # 17 - Broken pincers drop from Crayfish on death (death_event)
        'id': 17, 'done': False, 'room': 999, 'item_name': 'none',
        'first_time_text': "After you deliver the killing blow, the crayfish shudders and extends its pincers towards you. A crack like a thunder peal reverberates through the water, and the deadly pincers break off the crayfish's forelimbs.",
        'already_done_text': 'You fit the pincers over your claws.',
    },
    {   # 18 - Use pincers (weapon flavor text)
        'id': 18, 'done': False, 'room': 999, 'item_name': 'pincers',
        'first_time_text': 'You snap your powerful pincers.',
        'already_done_text': 'You snap your powerful pincers.',
    },
    {   # 19 - Use broken pincers: upgrade to mega-turtle, release Sea serpent
        'id': 19, 'done': False, 'room': 999, 'item_name': 'broken pincers',
        'first_time_text': 'You fit the pincers over your claws.',
        'already_done_text': 'You fit the pincers over your claws.',
    },
    {   # 20 - Gem of restoration drops from Sea serpent on death (death_event)
        'id': 20, 'done': False, 'room': 999, 'item_name': 'none',
        'first_time_text': "With your final deadly snip, you sever the body of the sea serpent. A large sapphire falls out of the its belly. You hear a voice from within,\n\n\t'Take the Gem of restoration. When you are ready, use it to return to the land above.'",
        'already_done_text': 'Your death blow produced the gem.',
    },
    {   # 21 - Use gem of restoration: end game
        'id': 21, 'done': False, 'room': 999, 'item_name': 'gem of restoration',
        'first_time_text': 'As you concentrate while clutching the gem, you feel the might of turtle power ebb from your being. You return to your human form, and find yourself transported to a safe, dry place.',
        'already_done_text': 'You already used the gem.',
    },
    {   # 22 - Read faded note (partial text)
        'id': 22, 'done': False, 'room': 999, 'item_name': 'faded note',
        'first_time_text': "You try to make sense of the partial text on the once-crumpled note. It reads:\n\n"
                           "\t'Our lake has been overtaken by\n"
                           "\t This creature of the sea has\n"
                           "\t Only the one who wears the rin\n"
                           "\t The one who bears symbols of\n"
                           "\t Peril now fills the lake. If y\n"
                           "\t Find the guardians, remove th",
        'already_done_text': "You try to make sense of the partial text on the once-crumpled note. It reads:\n\n"
                             "\t'Our lake has been overtaken by\n"
                             "\t This creature of the sea has\n"
                             "\t Only the one who wears the rin\n"
                             "\t The one who bears symbols of\n"
                             "\t Peril now fills the lake. If y\n"
                             "\t Find the guardians, remove th",
    },
    {   # 23 - Read note (full text after faucet reveal)
        'id': 23, 'done': False, 'room': 999, 'item_name': 'note',
        'first_time_text': "You read the note:\n\n"
                           "\t'Our lake has been overtaken by a venomous tyrant.\n"
                           "\t This creature of the sea has corrupted the waters and installed three hidden guardians.\n"
                           "\t Only the one who wears the ring of power may enter the lake and save it.\n"
                           "\t The one who bears symbols of great warriors can forge the ring at the water's edge.\n"
                           "\t Peril now fills the lake. If you can emerge, even for a moment, you may find relief, or more danger.\n"
                           "\t Find the guardians, remove them, and face the usurper. Purge this being from the lake to redeem it.'",
        'already_done_text': "You read the note:It now reads:\n\n"
                             "\t'Our lake has been overtaken by a venomous tyrant.\n"
                             "\t This creature of the sea has corrupted the waters and installed three hidden guardians.\n"
                             "\t Only the one who wears the ring of power may enter the lake and save it.\n"
                             "\t The one who bears symbols of great warriors can forge the ring at the water's edge.\n"
                             "\t Peril now fills the lake. If you can emerge, even for a moment, you may find relief, or more danger.\n"
                             "\t Find the guardians, remove them, and face the usurper. Purge this being from the lake to redeem it.'",
    },
    {   # 24 - Use kitchen sink: flavor text
        'id': 24, 'done': False, 'room': 3, 'item_name': 'kitchen sink',
        'first_time_text': 'You turn the faucet on and off. The miracle of indoor plumbing.',
        'already_done_text': 'You let the water run over your hands. Feels nice.',
    },
    {   # 25 - Use shell (defensive): flavor text
        'id': 25, 'done': False, 'room': 999, 'item_name': 'shell',
        'first_time_text': 'You pull your limbs and head deep into your shell.',
        'already_done_text': 'You pull your limbs and head deep into your shell.',
    },
    {   # 26 - Use remote (no batteries): flavor text
        'id': 26, 'done': False, 'room': 999, 'item_name': 'remote',
        "first_time_text": "You point the remote and press its buttons. Without batteries, it doesn't do anything.",
        'already_done_text': 'The remote is useless without two AA batteries.',
    },
    {   # 27 - Use batteries: flavor text (no device uses C batteries)
        'id': 27, 'done': False, 'room': 999, 'item_name': 'batteries',
        'first_time_text': 'You try to find a use for the C batteries, but nothing seems to need them.',
        'already_done_text': 'Does anything even use C batteries?',
    },
    {   # 28 - Use leather boot: flavor text
        'id': 28, 'done': False, 'room': 999, 'item_name': 'leather boot',
        'first_time_text': "Back when you had human feet, this boot might have fit you. Now it's just ridiculous.",
        'already_done_text': "Without it's pair, this mushy boot is just sad.",
    },
    {   # 29 - Use wild celery: flavor text
        'id': 29, 'done': False, 'room': 999, 'item_name': 'wild celery',
        'first_time_text': 'All you can do is swim around and through its curly stalks.',
        'already_done_text': "There's not much else you can do with it besides admire how peaceful it is.",
    },
    {   # 30 - Use clam shell (room 17): flavor text nudge
        'id': 30, 'done': False, 'room': 17, 'item_name': 'clam shell',
        'first_time_text': 'With all your might, you try to pry open the shell. Not gonna happen.',
        'already_done_text': 'Though it is closed now, something tells you there\'s a way to open the shell.',
    },
]


def _check_shell_buttons(current_room, state):
    """Called after any shell button is pressed; opens grotto when all three are done."""
    done_count = sum(1 for i in [6, 7, 8] if state.events[i]['done'])
    if done_count == 3:
        print('This time a loud creaking noise rumbles through the water. Something has changed somewhere.')
        state.world[36]['visible'] = True
        state.world[17]['desc'] = (
            'Tall reeds are thick in the northern edge of the lake. As you swim through the water, you see the surface above. '
            'The massive clam shell has opened revealing a passage to the north. '
            'The shallows extend to the east and to the west. Another cave entrance lies below.'
        )
        state.world[17]['exits'] = {'n': 36, 'e': 16, 'w': 18, 'd': 25}
        state.delete_thing('clam shell')
    elif done_count == 2:
        print('A short, grinding sound is heard from elsewhere in the lake. You start to sense a pattern.')
    else:
        print('You hear a dull click in the distance.')


def handle_event(event_id, current_room, state):
    """Execute the side effects for the given event id.

    Reads and writes: state.things, state.world, state.events, state.player_hp,
                      state.room, state.creatures, state.inventory_quantity.
    Calls: state.delete_thing(name), state.add_thing(item_dict).
    Both are wired up in step 2 (GameState).
    """
    event = state.events[event_id]

    # --- Simple events: print text and mark done ---
    if event_id in [5, 18, 22, 23, 24, 25, 26, 27, 28, 29, 30]:
        print(event['first_time_text'])
        event['done'] = True

    # --- Filter on sink: create enhanced faucet ---
    elif event_id == 0:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'enhanced faucet', 'prefix': 'an',
            'description': 'The kitchen sink is now fitted with a gleaming filter. The water appears to clarify everything it touches.',
            'location': 3, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('filter')
        state.delete_thing('kitchen sink')

    # --- Enhanced faucet: reveal note, open front door (needs faded note in room or on person) ---
    elif event_id == 1:
        note = next((t for t in state.things if t['name'] == 'faded note'), None)
        if note and (note['on_person'] or note['location'] == current_room):
            print(event['first_time_text'])
            event['done'] = True
            state.add_thing({
                'name': 'note', 'prefix': 'the',
                'description': "After rinsing the faded note in the filtered water, the text becomes sharper and more words are visible! It now reads:\n\n"
                               "\t'Our lake has been overtaken by a venomous tyrant.\n"
                               "\t This creature of the sea has corrupted the waters and installed three hidden guardians.\n"
                               "\t Only the one who wears the ring of power may enter the lake and save it.\n"
                               "\t The one who bears symbols of great warriors can forge the ring at the water's edge.\n"
                               "\t Peril now fills the lake. If you can emerge, even for a moment, you may find relief, or more danger.\n"
                               "\t Find the guardians, remove them, and face the usurper. Purge this being from the lake to redeem it.'",
                'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': True,
            })
            state.delete_thing('faded note')
            state.world[9]['visible'] = True
            state.world[0]['desc'] = (
                'This entryway is just inside the front door of your home. Most of the house is accessible from here. '
                'The dining room lies to the west, the living room is south, a stairway leads us to the second-level rooms, '
                'and a door to the garage is east. On the northern wall is the front door to the outdoors.'
            )
            state.world[0]['exits'] = {'n': 9, 's': 4, 'w': 1, 'e': 5, 'u': 6}
        else:
            print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')

    # --- Wear shirt: move to on_person (done never set True) ---
    elif event_id == 2:
        print(event['first_time_text'])
        for thing in state.things:
            if thing['name'].lower() == 'shirt':
                if thing['on_person']:
                    return
                thing['on_person'] = True
                state.inventory_quantity += 1

    # --- Hex nut on pier: forge ring of power if wearing shirt ---
    elif event_id == 3:
        hex_nut = any(
            t['name'] == 'hex nut' and (t['location'] == current_room or t['on_person'])
            for t in state.things
        )
        shirt_worn = any(t['name'] == 'shirt' and t['on_person'] for t in state.things)
        if hex_nut and shirt_worn:
            state.add_thing({
                'name': 'ring of power', 'prefix': 'the',
                'description': 'This silver ring glows and emits a faint hum.',
                'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': True,
            })
            state.delete_thing('hex nut')
            state.delete_thing('shirt')
            state.world[12]['visible'] = True
            state.world[11]['desc'] = (
                'The splintered planks of the pier jut into the murky lake. Rocks, lily pads, and cattails dot the surrounding waters. '
                'Dry land is to the southwest. You feel drawn into the water below.'
            )
            state.world[11]['exits'] = {'sw': 10, 'd': 12}
            print(event['first_time_text'])
        else:
            print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')

    # --- Trident on air bladder: pop, reveal Industrial pipe ---
    elif event_id == 4:
        print(event['first_time_text'])
        event['done'] = True
        state.world[37]['visible'] = True
        state.world[22]['desc'] = 'Jagged rocks make up the walls of this tunnel that runs from the southwest to the northeast. Now that the bladder is removed, a circular opening leads east.'
        state.world[22]['exits'] = {'e': 37, 'sw': 21, 'ne': 23}
        state.delete_thing('air bladder')

    # --- Shell buttons: press guardian shell; open grotto when all three pressed ---
    elif event_id in [6, 7, 8]:
        print(event['first_time_text'])
        event['done'] = True
        _check_shell_buttons(current_room, state)

    # --- Eat duckweed: heal 40-60 HP ---
    elif event_id == 9:
        print(event['first_time_text'])
        event['done'] = True
        state.player_hp = min(state.player_hp + random.randrange(0, 21) + 40, 100)
        state.delete_thing('duckweed')

    # --- Eat lake lettuce: heal 45-65 HP ---
    elif event_id == 10:
        print(event['first_time_text'])
        event['done'] = True
        state.player_hp = min(state.player_hp + random.randrange(0, 21) + 45, 100)
        state.delete_thing('lake lettuce')

    # --- Eat water grubs: heal 50-70 HP ---
    elif event_id == 11:
        print(event['first_time_text'])
        event['done'] = True
        state.player_hp = min(state.player_hp + random.randrange(0, 21) + 50, 100)
        state.delete_thing('water grubs')

    # --- Trident drops from Mermaid on death ---
    elif event_id == 12:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'trident', 'prefix': 'a',
            'description': "This three-pronged spear looks like it could puncture anything. Unfortunately, your short turtle-arms can't use it as a weapon. Still, you might find a use for it.",
            'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })

    # --- Curious blob in fountain: extract rusty key ---
    elif event_id == 13:
        print(event['first_time_text'])
        event['done'] = True
        state.add_thing({
            'name': 'rusty key', 'prefix': 'the',
            'description': "It's a key. It's rusty. There has to be a use for it.",
            'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('curious blob')

    # --- Curious blob drops from Algae on death ---
    elif event_id == 14:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'curious blob', 'prefix': 'a',
            'description': "Yuck. It looks like a huge booger. If it didn't seem important, you would get far away from the sickly glob.",
            'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })

    # --- Use fountain: extract rusty key only if curious blob is present in room or on person ---
    elif event_id == 15:
        blob = next((t for t in state.things if t['name'].lower() == 'curious blob'), None)
        if blob and (blob['location'] == current_room or blob['on_person']):
            print(event['first_time_text'])
            event['done'] = True
            state.add_thing({
                'name': 'rusty key', 'prefix': 'the',
                'description': "It's a key. It's rusty. There has to be a use for it.",
                'location': current_room, 'on_person': True, 'moveable': True, 'is_weapon': False, 'no_drop': False,
            })
            state.delete_thing('curious blob')
        else:
            print('You hold your claws under the cleansing stream. Feels nice.')

    # --- Rusty key on lobster trap: unlock cage, release Crayfish ---
    elif event_id == 16:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'busted trap', 'prefix': 'a',
            'description': 'The lobster trap is a heap of twisted wire and splintered wood planks. It is still connected to the rope from above.',
            'location': 40, 'on_person': False, 'moveable': False, 'is_weapon': False, 'no_drop': False,
        })
        state.delete_thing('lobster trap')
        state.creatures.append({
            'id': 2, 'name': 'Crayfish',
            'description': 'This hulking creature darts about, snapping its pincers wildly.',
            'room': 40, 'max_hp': 120, 'current_hp': 120, 'is_dead': False, 'is_hostile': True,
            'status_neutral': 'It swims in circles around you.', 'status_hostile': 'It readies to attack.',
            'damage': 15, 'hit_bonus': 10, 'attack_chance': 70, 'is_fatigued': False,
            'death_event': 17, 'was_seen': False,
            'dead_description': 'The thick-shelled crustacean floats listlessly on the lake floor.',
        })

    # --- Broken pincers drop from Crayfish on death ---
    elif event_id == 17:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'broken pincers', 'prefix': 'the',
            'description': 'It looks like you could slide your claws into these dark weapons of the crayfish.',
            'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })

    # --- Use broken pincers: become mega-turtle, release Sea serpent ---
    elif event_id == 19:
        print(event['first_time_text'])
        event['done'] = True
        state.add_thing({
            'name': 'pincers', 'prefix': 'your',
            'description': 'These claw-like appendages are gleaming black. The inner grip is dotted with a cutting edge of gnarly teeth.',
            'location': current_room, 'on_person': True, 'moveable': True,
            'is_weapon': True, 'base_damage': 20, 'damage': 50, 'hit_bonus': 35, 'no_drop': True,
        })
        state.delete_thing('broken pincers')
        state.delete_thing('claws')
        print('A familiar surge of mystical energy runs through you. Your shell is harder, your limbs are more powerful, and your health is restored. You feel invincible! And my, what deadly pincers you have.')
        print('You are now a MEGA-TURTLE. When in combat, use your PINCERS to attack and your SHELL for protection.')
        state.player_hp = 100
        state.creatures.append({
            'id': 2, 'name': 'Sea serpent',
            'description': 'This terrifying snake has deep blue scales and penetrating yellow eyes. A flame-red tongue flickers impatiently. As its tremendous length coils over itself, you are convinced it belongs in a much larger body of water.',
            'room': 35, 'max_hp': 300, 'current_hp': 300, 'is_dead': False, 'is_hostile': False,
            'status_neutral': 'It flashes its lethal fangs in a cruel smirk.', 'status_hostile': 'It is poised to strike!',
            'damage': 5, 'hit_bonus': 10, 'attack_chance': 65, 'is_fatigued': False,
            'death_event': 20, 'was_seen': False,
            'dead_description': 'The grisly body of the snake winds around the lake floor. What a mess.',
        })
        if current_room == 35:
            print('\nFrom the hole in the eastern wall, a massive serpent slithers into the cavern.')
        else:
            print('\nYou hear an unsettling sound in the distance. Something slithers in the deep.')

    # --- Gem of restoration drops from Sea serpent on death ---
    elif event_id == 20:
        print(event['first_time_text'])
        event['done'] = True
        state.things.append({
            'name': 'gem of restoration', 'prefix': 'the',
            'description': "An irrevocable power emanates from the deep blue depths of this jewel. One you use it, there's no turning back.",
            'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False, 'no_drop': False,
        })

    # --- Use gem of restoration: end game ---
    elif event_id == 21:
        print(event['first_time_text'])
        state.room = EXIT_ROOM
        event['done'] = True


def handle_special(current_room, state):
    """Turtle transformation at surface; random hazards/benefits on resting spots; lake ambience."""
    # Room 12 (Surface): transform into turtle on first entry
    if current_room == 12 and not state.special_done[0]['done']:
        print('When you enter the water, a surge of mystical energy runs through you. Your whole being quickly transforms into something smaller with a hard-back SHELL and fierce CLAWS.')
        print('You are a TURTLE. When in combat, use your claws to attack and your shell for protection.')
        for thing in state.things:
            if thing['name'] == 'claws':
                thing['on_person'] = True
                state.inventory_quantity += 1
            elif thing['name'] == 'shell':
                thing['on_person'] = True
                state.inventory_quantity += 1
        state.special_done[0]['done'] = True

    # Rooms 30-33 (surface resting spots): random event on first visit
    if current_room in [30, 31, 32, 33] and not state.locale_visited:
        special_chance = random.randrange(1, 101)
        if special_chance >= 67:  # harm
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
            damage = random.randrange(2, 9)
            state.player_hp -= damage
            if state.player_hp <= 0:
                state.player_hp = 1

        elif special_chance >= 34:  # benefit
            special_type = random.randrange(1, 4)
            if special_type == 1:
                print('The clouds part, and a warm sunbeam lands on your shell. The heat gives you a delightful boost.')
            elif special_type == 2:
                print('A plump fly buzzes into your open mouth. You chew and swallow the protein-filled treat. Yum!')
            else:
                print("You spot a sneaky teenager on the shore, holding their phone towards you. They snap a pic and post it. You're famous! Well, Internet famous.")
            heal = random.randrange(2, 11)
            state.player_hp = min(state.player_hp + heal, 100)

        else:  # nothing happens
            special_type = random.randrange(1, 4)
            if special_type == 1:
                print('You enjoy a moment of peace.')
            elif special_type == 2:
                print('Looking around at the still water gives you a moment to catch your breath.')
            else:
                print('A gentle breeze plays across your round body. Feels nice.')

    # Inside lake rooms 13-29: random ambient flavor when no mobs are present
    if not state.room_has_mobs and 12 < current_room < 30:
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
