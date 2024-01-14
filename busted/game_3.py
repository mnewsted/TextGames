#! python3
# TextGames Space Adventure - Game 3
# version 1.3
# description: separating game content from engine. adding rooms and items.

def do_event(event_id, current_room):
    global inventory_quantity
    global game_choice
    global player_hp
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
                       'on_person': True, 'moveable': True, 'is_weapon': False})
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
                       'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False})
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
                       'on_person': True, 'moveable': True, 'is_weapon': False})
        inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
        # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
        things.append({'name': 'quarters keycard', 'prefix': 'a',
                       'description': 'After wiping it clean, you see this keycard has the words \'Crew Quarters\' printed on it.',
                       'location': 10, 'on_person': False, 'moveable': True, 'is_weapon': False})
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
                       'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False})
    if event_id in [13]:
        print(events[event_id]['first_time_text'])
        events[event_id]['done'] = True
        # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
        things.append({'name': 'soldier eye', 'prefix': 'a',
                       'description': 'You don\'t feel great about how you got it, but the eyeball is pretty cool.',
                       'location': 39, 'on_person': True, 'moveable': True, 'is_weapon': False})
        inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
        # replace existing soldier with a modified version
        delete_thing('fallen soldier')
        things.append({'name': 'fallen soldier', 'prefix': 'a',
                        'description': 'This dead crewmate is bent backwards, leaning on the countertop. They have the insignia and fatigues of a tactical combat specialist. '
                        'Unlike the other bodies you encountered, this one seems frozen in shock, face up with one eye and mouth wide open.',
                        'location': 39, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0})
    # use large stimpack
    if event_id in [15]:
        print(events[event_id]['first_time_text'])
        events[event_id]['done'] = True
        player_hp = player_hp + 90
        if player_hp > 100:
            player_hp = 100
        things.append({'name': 'empty large stimpack', 'prefix': 'an',
                       'description': 'There\'s not much to do with the large stimpack now that it is drained.', 'location': current_room,
                       'on_person': True, 'moveable': True, 'is_weapon': False})
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
                       'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False})
    # use wound salve
    if event_id in [23]:
        print(events[event_id]['first_time_text'])
        events[event_id]['done'] = True
        player_hp = player_hp + 35
        if player_hp > 100:
            player_hp = 100
        things.append({'name': 'used wound salve', 'prefix': 'a',
                       'description': 'The wound salve jar is empty. What a shame.', 'location': current_room,
                       'on_person': True, 'moveable': True, 'is_weapon': False})
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
                           'location': current_room, 'on_person': False, 'moveable': True, 'is_weapon': False})
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
        launch_code = str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + 'L07A' + str(random.randrange(0, 9)) + str(random.randrange(0, 9))
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
                   'location': 45, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0})
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
                   'location': 999, 'on_person': True, 'moveable': True, 'is_weapon': True, 'base_damage': 25, 'damage': 30, 'hit_bonus': 45})
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
                       'on_person': True, 'moveable': True, 'is_weapon': False})
        inventory_quantity = inventory_quantity + 1  ## add to inventory if appending thing on_person == True
        delete_thing('medium stimpack')
    # unclog toilet and create metal key
    if event_id in [42]:
        print(events[event_id]['first_time_text'])
        events[event_id]['done'] = True
        # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM OR USE current_room VARIABLE
        things.append({'name': 'metal key', 'prefix': 'a', 'description': 'This small, silvery key has all the notches and grooves you expect to see in something that could unlock a door.',
                       'location': 47, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0})
        # remove old toilet create new one
        delete_thing('clogged toilet')
        things.append({'name': 'toilet', 'prefix': 'a',
                       'description': 'The flush mechanism still doesn\'t work, but at least it is empty.',
                       'location': 47, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
                       'hit_bonus': 0})
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


def do_special(current_room):
    global player_hp
    global special_done

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

world = []
things = []
events = []
creatures = []
special_rooms = []
special_done = []

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
world.insert( 46, {'visible': True, 'name': 'Toilet Bank 1', 'prefix': 'in', 'name2': '',
                   'desc': 'An impressive number of toilets and bidets are discretely concealed within ceiling-to-floor privacy screens. The Crew Facilities are accessible to the south.',
                   'exits': {'s': 31}})
world.insert( 47, {'visible': True, 'name': 'Toilet Bank 2', 'prefix': 'in', 'name2': '',
                   'desc': 'An impressive number of toilets and bidets are discretely concealed within ceiling-to-floor privacy screens. The Crew Facilities are accessible to the north.',
                   'exits': {'n': 31}})
world.insert( 48, {'visible': True, 'name': 'Custodial Supplies room', 'prefix': 'in the', 'name2': '',
                   'desc': 'This dingy space contains an array of maintenance tools and equipment. To the northeast is the Funneling hallway. On the west side of the room is a door marked Workroom. '
                           'It is locked, but the door knob has an old-fashioned keyhole in it.', 'exits': {'ne': 12}})
world.insert( 49, {'visible': False, 'name': 'Workroom', 'prefix': 'in the', 'name2': '',
                   'desc': 'The familiar workroom has decent lighting and ample space to fix or build all kinds of things. '
                           'The only exit is back east to the Custodial Supplies room.', 'exits': {'e': 48}})



things.append({'name': 'food tray', 'prefix': 'a',
               'description': 'The empty food tray has some heft to it. The metal edge looks mean.',
               'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': 10,
               'damage': 10, 'hit_bonus': 25})
things.append({'name': 'stimpack', 'prefix': 'a',
               'description': 'A small vial of clear liquid has a tiny needle on one end and a red heart decal on the side.',
               'location': 3, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'breathing mask', 'prefix': 'a',
               'description': 'The compact device looks like it would fit nicely on your face if you pick it up or use it.',
               'location': 3, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'digipad1', 'prefix': 'a',
               'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                              '\n\tAfter we were attacked, I dragged you in here and set the door to lock from the inside.'
                              '\n\tYou can get out but be careful: most of the crew is dead. Those that survived are, well, dangerous.'
                              '\n\tUse whatever you can to survive. You gotta get off this ship. -B',
               'location': 0, 'on_person': False, 'moveable': True, 'is_weapon': False})
things.append({'name': 'digipad2', 'prefix': 'a',
               'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                              '\n\tSome kind of virus swept through the ship. It killed most of the crew. Others were corrupted.'
                              '\n\tThey do not need oxygen. They are diverting the ship\'s oxygen for some other purpose.'
                              '\n\tI preserved the atmosphere settings on the Detention Level, but other places on the ship are probably bad. -B',
               'location': 2, 'on_person': False, 'moveable': True, 'is_weapon': False})
things.append({'name': 'wrench', 'prefix': 'a',
               'description': 'The heavy tool is rusted, but it could do some real damage.',
               'location': 17, 'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': 15,
               'damage': 15, 'hit_bonus': 30})
things.append({'name': 'fuel cell', 'prefix': 'a',
               'description': 'This metallic cylinder emits a strange bluish glow from a slit on each end. A warning label reads: DANGER - Will burn through organic matter.',
               'location': 16, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'corpse', 'prefix': 'a',
               'description': 'The body of one of your crewmates lies on the floor, contorted in an unnatural pose. Every inch of their body is covered in a wet, dark gray-green substance. '
                              'It is translucent and looks hard, almost stone-like.',
               'location': 10, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'digipad5', 'prefix': 'a',
               'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                              '\n\tThe virus doesn\'t act the same on everybody. It doesn\'t make sense.'
                              '\n\tI saw Jackson from Combat Services collapse. When she did, a jade crystal coating formed over her skin.'
                              '\n\tOthers went into zombie mode and started attacking. -A',
               'location': 8, 'on_person': False, 'moveable': True, 'is_weapon': False})
things.append({'name': 'allen claw', 'prefix': 'an',
               'description': 'This shiny, angular piece of metal appears to have been fashioned for a specific purpose.',
               'location': 41, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'smooth bar', 'prefix': 'a',
               'description': 'This rod is painted orange. It has fittings on both ends.',
               'location': 31, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append(
    {'name': 'gummy grip', 'prefix': 'a', 'description': 'The short pipe has a cushioned yet tackified surface.',
     'location': 27, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0})
things.append({'name': 'dented tricorder', 'prefix': 'a',
               'description': 'This banged-up scanner must be good for something. It still beeps!',
               'location': 32, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'lockbox', 'prefix': 'a',
               'description': 'There are cryptic symbols on this oblong box. The lid is fastened tight, but a square keyhole looks promising.',
               'location': 18, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'scalpel', 'prefix': 'a',
               'description': 'The surgical blade is short but exceedingly sharp. It would be very effective at a targeted procedure, but it could also do some damage in a fight if it connected.',
               'location': 37, 'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': 10,
               'damage': 25,
               'hit_bonus': 15})
things.append({'name': 'fallen soldier', 'prefix': 'a',
               'description': 'This dead crewmate is bent backwards, leaning on the countertop. They have the insignia and fatigues of a tactical combat specialist. '
                              'Unlike the other bodies you encountered, this one seems frozen in shock, face up with eyes and mouth wide open.',
               'location': 39, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'large stimpack', 'prefix': 'a',
               'description': 'This device has 3 compact barrels of clear liquid that funnel into a small needle. You are comforted by the cheerful red heart logo on the top, '
                              'and the encouraging label that reads, "Massive vitality boost."',
               'location': 36, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'digipad4', 'prefix': 'a',
               'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                              '\n\tThey say you can see it in the eyes when they\'re infected. They get all hazy.'
                              '\n\tIf that\'s true, then it\'s happening to me. I can\'t see my own reflection any more. -L',
               'location': 38, 'on_person': False, 'moveable': True, 'is_weapon': False})
things.append({'name': 'hot sauce', 'prefix': 'a',
               'description': 'This small bottle has a picture of a burning crescent-shaped pepper. "One drop\'ll do ya!"',
               'location': 40, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append(
    {'name': 'mayonnaise', 'prefix': 'a', 'description': 'The large jar of eggy, white, goop is still half-full.',
     'location': 40, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0})
things.append({'name': 'pear powder', 'prefix': 'a',
               'description': 'A hand-written label on this see-through bag describes the sparkly, yellow granules inside the flavor pouch.',
               'location': 40, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'digipad3', 'prefix': 'a',
               'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                              '\n\tTraining today in Systems Control. Learned how to activate locked down systems.'
                              '\n\tThey got some real Rube Goldberg protocols. The lever that works the controls is'
                              '\n\tassembled from three parts in storage on the ship. How is that secure? -M',
               'location': 29, 'on_person': False, 'moveable': True, 'is_weapon': False})
things.append({'name': 'phaser', 'prefix': 'a',
               'description': 'The V-8 phaser pistol is a reliable mid- to close-range weapon.',
               'location': 26, 'on_person': False, 'moveable': True, 'is_weapon': True, 'base_damage': 20,
               'damage': 25, 'hit_bonus': 40})
things.append({'name': 'wound salve', 'prefix': 'a',
               'description': 'The label on the opaque brown jar reads, "Apply liberally to cuts, welts, and lacerations." Inside is a substance that looks like pink jelly.',
               'location': 27, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'digipad8', 'prefix': 'a',
               # update this text
               'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                              '\n\tThose infected, zombies, whatever--they do not stop.'
                              '\n\tMe and Barb held off 6 of them in the mess hall. Don\'t know why but food seemed to make them weak.'
                              '\n\tOr maybe it just distracted them. Hope somebody sees this. -X',
               'location': 24, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'code generator', 'prefix': 'a',
               'description': 'Nestled between navigation consoles is a device labeled "Escape Pod Launch Code Generator." It looks like an old-timey vending machine. There\'s a shiny red button and a digital display.',
               'location': 44, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'lockdown console', 'prefix': 'the',
               'description': 'The lockdown console has a small screen that reads: \n\t"LOCKDOWN ENGAGED - Offline systems: Hangar elevator, Deepspace Communications, Escape pods"'
                              '\nThere does not appear to be any way to interact with the console, but there is an empty lever socket just below the screen.',
               'location': 45, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'launch controls', 'prefix': 'the',
               'description': 'The launch controls look like a small terminal. There\'s a screen and a keyboard.',
               'location': 21, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'launch console', 'prefix': 'the',
               'description': 'The launch console looks like a small terminal. There\'s a screen and a keyboard.',
               'location': 22, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'dead crewmate', 'prefix': 'a',
               'description': 'You recognize Petty Officer Smith from your time at the academy. He was always in motion. Now his body lies still. It looks like he suffered several blaster wounds.',
               'location': 32, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'dead engineer', 'prefix': 'a',
               'description': 'It\'s hard to look at the engineer. Her arm is bending the wrong way, and her head was hit hard by something heavy. The damage is so extensive you can\'t even recognize her.',
               'location': 15, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'retina scanner', 'prefix': 'a',
               'description': 'The scanner is built-into a panel next to the elevator door. '
                              'It sits at about eye-level and sheds a dull red glow.',
               'location': 11, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'phaser booster', 'prefix': 'a',
               'description': 'The booster is a shiny gray widget. In small print it reads, '
                              '"Turns your V-8 into a V-9!"',
               'location': 7, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'medium stimpack', 'prefix': 'a',
               'description': 'The double vials have red hearts etched into their sides. There is only one needle, thankfully.',
               'location': 30, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0,
               'hit_bonus': 0})
things.append({'name': 'clogged toilet', 'prefix': 'a',
               'description': 'The flush mechanism is not responsive. The bowl is stuffed with what looks like a very wet dark blue cloth.',
               'location': 47, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0})
things.append({'name': 'astroplunger', 'prefix': 'an', 'description': 'Some technology can\'t be improved upon. '
               'Despite its fancy name, the wooden handle and dark rubber bulb are fashioned in the classic design.',
               'location': 48, 'on_person': False, 'moveable': True, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0})
things.append({'name': 'workbench', 'prefix': 'the', 'description': 'With this state-of-the-art quantum-precision workbench, '
                                                                    'there\'s nothing you can\'t build! The urge to create is almost overwhelming.',
               'location': 49, 'on_person': False, 'moveable': False, 'is_weapon': False, 'damage': 0, 'hit_bonus': 0})
things.append({'name': 'digipad9', 'prefix': 'a',
               'description': 'Like other digipads you\'ve seen, this one contains messages sent by your crewmates.'
                              '\n\tThey\'re hunting the custodial staff. I guess it\'s because we have access to so much of the ship.'
                              '\n\tSome of the team is hiding their uniforms. I guess the dark blue color gives us away. -B',
               'location': 6, 'on_person': False, 'moveable': True, 'is_weapon': False})
things.append({'name': 'workbench manual', 'prefix': 'a',
               'description': 'You scan the manual for relevant information.'
                              '\n\t...Holding high-heat materials requires gloves reinforced with non-conductive fibers...'
                              '\n\t...A workbench is only as effective as it is clean. Buy our patented Bleakwipes to keep your workspace factory-pure...'
                              '\n\t...Most levers can be constructed with a bar, a grip for holding, and some kind of tip that will connect to...'
                              '\n\t...Fuel cell containers are not worth modifying. StarClunk makes the best...',
               'location': 12, 'on_person': False, 'moveable': True, 'is_weapon': False})



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

# sets the special event to apply to rooms 5-46
for i in range(5, 46):
    special_rooms.append(i)
