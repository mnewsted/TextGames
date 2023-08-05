#! python3
# text_game
# version 1.2.8.5
# description improvements and formatting fix after user testing

# functions
def locale(current_room):
    print('You are ' + world[current_room]['prefix'] + ' ' + world[current_room]['name'] + '.')
    print(world[current_room]['desc'])
    show_things(current_room)

def look_around(current_room):
    print('You are ' + world[current_room]['prefix'] + ' ' + world[current_room]['name'] + '.')
    print(world[current_room]['desc'])
    show_exits(current_room)
    show_things(current_room)

def examine_item(current_room):
    global inventory_quantity
    global room_has_items
    global target

    update_things_in_room(current_room)
    if target in available_targets(current_room):
        for thing in things:
            if thing['name'].lower() == target.lower():
                print(thing['description'])
        return

    if room_has_items or inventory_quantity > 0:
        available_choices = []
        print('Items you can examine:')
        if room_has_items:
            for thing in things:
                if (thing['location']==current_room and thing['on_person']==False):
                    print( thing['name'].capitalize() )
                    available_choices.append(thing['name'].lower())
        if inventory_quantity > 0:
            for thing in things:
                if (thing['on_person']==True):
                    print( thing['name'].capitalize() )
                    available_choices.append(thing['name'].lower())
        print('What item do you want to examine? (type the item name or press ENTER for none)')
        choice = input().lower()
        if choice == '':
            return
        while choice not in available_choices:
            print('That\'s not a valid choice. Try again.')
            print('What item do you want to examine? (type the item name or press ENTER for none)')
            choice = input().lower()
            if choice == '':
                return
        for thing in things:
            if thing['name'].lower() == choice:
                print(thing['description'])
    else:
        print('There isn\'t anything you examine here. Go find something!')


def show_things(current_room):
    global room_has_items
    visible_items = 0
    print('Visible items:')
    for thing in things:
        if (thing['location']==current_room and thing['on_person']==False):
            print( thing['prefix'].capitalize() + ' ' + thing['name'] )
            visible_items = visible_items + 1
            room_has_items = True
    if visible_items == 0:
        print('You don\'t see anything special.')
        room_has_items = False

def update_things_in_room(current_room):
    global room_has_items
    visible_items = 0
    for thing in things:
        if (thing['location']==current_room and thing['on_person']==False):
            visible_items = visible_items + 1
            room_has_items = True
    if visible_items == 0:
        room_has_items = False


def show_inventory(quantity):
    if quantity > 0:
        print('You are carrying:')
        for thing in things:
            if thing['on_person'] == True:
                print( thing['prefix'].capitalize() + ' ' + thing['name'] )
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
            if (thing['location']==current_room and thing['on_person']==False):
                available_choices.append(thing['name'].lower())
        for thing in things:
            if thing['name'].lower() == target.lower():
                if thing['moveable'] == True:
                    thing['on_person'] = True
                    inventory_quantity = inventory_quantity + 1
                    print('You pick up ' + thing['prefix'] + ' ' + thing['name'] + '.')
                    return
                else:
                    print('You can\'t take ' + thing['prefix'] + ' ' + thing['name'] + '.')
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
                    print('You pick up ' + thing['prefix'] + ' ' + thing['name'] + '.')
                else:
                    print('You can\'t take ' + thing['prefix'] + ' ' + thing['name'] + '.')
    else:
        print('There aren\'t any items worth taking.')

def drop_item(current_room):
    global inventory_quantity
    global target

    if inventory_quantity == 0:
        print('You aren\'t carrying anything.')
        return

    update_things_in_room(current_room)
    if target in available_targets(current_room):
        for thing in things:
            if thing['name'].lower() == target.lower():
               thing['on_person'] = False
               thing['location'] = current_room
               user_has_items = True
               print('You drop ' + thing['prefix'] + ' ' + thing['name'] + '.')
               inventory_quantity = inventory_quantity - 1
        return
    else:
        print( '\"' + target + '\" is not in your inventory.')

    if inventory_quantity > 0:
        available_choices = []
        print('Items you are carrying:')
        for thing in things:
            if (thing['on_person']==True):
                print( thing['name'].capitalize() )
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
               print('You drop ' + thing['prefix'] + ' ' + thing['name'] + '.')
               inventory_quantity = inventory_quantity - 1
    else:
        print('You aren\'t carrying anything.')

def use_item(current_room):
    global inventory_quantity
    global room_has_items
    global target

    update_things_in_room(current_room)
    if target in available_targets(current_room):
        check_event(current_room, target.lower())
        return
    else:
        print( '\"' + target + '\" is not available to use.')
        
    if room_has_items or inventory_quantity > 0:
        available_choices = []
        print('Items you can use:')
        if room_has_items:
            for thing in things:
                if (thing['location']==current_room and thing['on_person']==False):
                    print( thing['name'].capitalize() )
                    available_choices.append(thing['name'].lower())
        if inventory_quantity > 0:
            for thing in things:
                if (thing['on_person']==True):
                    print( thing['name'].capitalize() )
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
        check_event(current_room, choice)
    else:
        print('There isn\'t anything you can use here.')


def available_targets(current_room):
    global inventory_quantity
    global room_has_items
    global target
    update_things_in_room(current_room)
    if room_has_items or inventory_quantity > 0:
        available_choices = []
        if room_has_items:
            for thing in things:
                if (thing['location']==current_room and thing['on_person']==False):
                    available_choices.append(thing['name'].lower())
        if inventory_quantity > 0:
            for thing in things:
                if (thing['on_person']==True):
                    available_choices.append(thing['name'].lower())
    return available_choices



def check_event(current_room, used_item):
    #print('DEBUG: checking what happens when using ' + used_item + ' in room # ' + str(current_room))
    #print(events)
    for event in events:
        if (event['room'] == current_room and event['item_name'].lower() == used_item):
            if event['done'] == False:
                do_event(event['id'])
                return
            else:
                print(event['already_done_text'])
                return
        if (event['room'] == 999 and event['item_name'].lower() == used_item):
            if event['done'] == False:
                do_event(event['id'])
                return
            else:
                print(event['already_done_text'])
                return
    print('Nothing happened. Maybe try somewhere else? Or try when another item is near?')
    
def do_event(event_id):
    global inventory_quantity
    global game_choice
    
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
            world[4]['desc'] = 'The grassy clearing at the end of the road is accented by a few tall trees. A new tree in the center has low, inviting branches. Part of the grass is bare along the southern edge, and it contains a strange etching of a house and a winged creature. The street is at the north end of the park, a trail leads through the trees to the west, and a meadow is to the east.'
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[4]['exits'] = { 'n':3, 'u':7, 'e':10, 'w':11}
            # find item and modify description
            item_index = ['tree kit' in i['name'] for i in things].index(True)
            things[item_index]['description'] = 'The empty tree kit box claims: \'Makes a real life tree in seconds! No digging required. For best results, use in an open area.\''
        # create portal
        if event_id in [7]:
            # birdhouse is prerequisite - if 'birdhouse' required because using robin in yard only has effect if birdhouse has been created
            if 'birdhouse' in str(things):
                print(events[event_id]['first_time_text'])
                events[event_id]['done'] = True
                # new room
                world[5]['visible'] = True
                # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
                world[4]['desc'] = 'The grassy clearing at the end of the road is dappled with light shining through the tall trees. A new tree in the center has low, inviting branches. Where the grass was worn to the south, you now see a brightly glowing portal! The street is at the north end of the park, a trail leads through the trees to the west, and a meadow is to the east.'
                # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
                world[4]['exits'] = { 'n':3, 'u':7, 's':5 }
                delete_thing('robin')
                inventory_quantity = inventory_quantity - 1
            else:
                print('Nothing happened.')
        # unlock gate
        if event_id in [20]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # new room
            world[13]['visible'] = True
            # updated connecting room description - BE CAREFUL TO BUILD ON PREVIOUS DESCRIPTION
            world[12]['desc'] = 'This gentle valley is surrounded by leafy trees and bushes. A path is visible to the west. To the north you see an open iron gate, beyond which lies the mouth of a cave.'
            # updated connecting room exits - BE CAREFUL TO INCLUDE PREVIOUS EXITS
            world[12]['exits'] = { 'e':11, 'n':13 }

        # create thing event template
        # remove bird from egg
        if event_id in [3]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({ 'name': 'robin', 'prefix': 'a', 'description': 'Its feathers are matted down by egg goo, and the baby bird is struggling to open its tiny eyes. It would be gross if it weren\'t so darn cute.', 'location': 7, 'on_person': True, 'moveable': True})
            things.append({ 'name': 'egg shell', 'prefix': 'an', 'description': 'There\'s little to do with the broken egg shell shards.', 'location': 7, 'on_person': False, 'moveable': True})
            delete_thing('egg')
        # reveal basement
        if event_id in [5]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({ 'name': 'toy house', 'prefix': 'a', 'description': 'This miniature colonial appears to be worn from play. You can imagine dolls going in and out of the doors and windows.', 'location': 6, 'on_person': False, 'moveable': True})
        # make birdhouse
        if event_id in [6]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({ 'name': 'birdhouse', 'prefix': 'the', 'description': 'The toy house resting atop the post will surely attract small, avian creatures.', 'location': 1, 'on_person': False, 'moveable': False})
            delete_thing('toy house')
        # make flashlight
        if event_id in [11]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({ 'name': 'flashlight', 'prefix': 'a', 'description': 'It\'s your standard issue flashlight. Looks like it could help you see in dark places, but it wouldn\'t do much elsewhere.', 'location': 9, 'on_person': False, 'moveable': True})
            delete_thing('coin')
        # make functional well
        if event_id in [17]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({ 'name': 'well', 'prefix': 'the', 'description': 'The well is still old, but now you can raise and lower the bucket.', 'location': 10, 'on_person': False, 'moveable': False})
            delete_thing('broken well')
            delete_thing('bucket')
        # make key
        if event_id in [18]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            # create new object - LOCATION CAN BE ANY IF ON_PERSON IS TRUE OTHERWISE MATCH LOCATION TO EVENT ROOM
            things.append({ 'name': 'key', 'prefix': 'a', 'description': 'The brass key is partially covered in moss. It feels heavy.', 'location': 10, 'on_person': False, 'moveable': True})
        # drop pebble
        if event_id in [19]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True
            delete_thing('pebble')
    elif game_choice == '2':
        if event_id in [0]:
            print(events[event_id]['first_time_text'])
            events[event_id]['done'] = True        

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
            print(full_direction(direction) + world[destination]['name'] )

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
        return(command[(space_index + 1):])

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
    print('\'Examine\' or \'X\' to inspect an item')
    print('\'Take\' to pick up an item and put it in your inventory')
    print('\'Drop\' to get rid of an item')
    print('You can type the action (use, examine, take, or drop) and the item, or just the action.')
    print('For example: If you want to use the apple, you can type \'use apple\' or \'use.\'')
    print('If you just type \'use,\' you will be asked what item you want to use.')
    print('')
    print('Other commands include:')
    print('\'L\' or \'Look\' to look around')
    print('\'Inv\' or \'inventory\' to see what you are carrying')
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
    world = []
    things = []
    events = []


def load_game(choice):
    global world
    global things
    global events
    global starting_room
    global exit_room
    global intro_text
    global outro_text
    clear_game_vars()
    if choice == '1':
        world.insert(0, { 'visible': True, 'name': 'House', 'prefix': 'in the', 'desc': 'This modest dwelling has one room on the ground floor. You can see the front yard to the east and the garage through a door to the south. One set of stairs leads up to the studio, and another goes down to the basement.', 'exits': {'e': 1, 's': 2, 'u': 8, 'd': 6}})
        world.insert(1, { 'visible': True, 'name': 'Yard', 'prefix': 'in the', 'desc': 'The grass in the front yard is browning, and the flowers look sad. You can go west to back into the house, or go south around the house to the garage. Outside of the yard to the east is a street.', 'exits': {'w': 0, 's': 2, 'e': 3}})
        world.insert(2, { 'visible': True, 'name': 'Garage', 'prefix': 'in the', 'desc': 'There is a musty smell, and oil stains cover the concrete floor. You can get to the house through the door to the north. The door to the yard is somehow stuck, but the main garage door to the east opens to the street.', 'exits': {'n': 0, 'e': 3}})
        world.insert(3, { 'visible': True, 'name': 'Street', 'prefix': 'on the', 'desc': 'You don\'t see any cars on this strikingly ordinary street. The house is nearby. To the north is the gate to the front yard, and the garage door is open to the west. You see a dusty junkyard to the east. Following the road south will bring you to a park.', 'exits': {'n': 1, 'w': 2, 'e': 9, 's': 4}})
        world.insert(4, { 'visible': True, 'name': 'Park', 'prefix': 'at the', 'desc': 'The wide, grassy clearing at the end of the road is accented by a few tall trees. Part of the grass is bare along the southern edge, and it contains a strange etching of a house and a winged creature. The street is at the north end of the park, a trail leads through the trees to the west, and a small meadow is to the east.', 'exits': {'n':3, 'e':10, 'w':11} })
        world.insert(5, { 'visible': False, 'name': 'Glowy portal', 'prefix': 'through the', 'desc': 'End description', 'exits': {}})
        world.insert(6, { 'visible': True, 'name': 'Basement', 'prefix': 'in the', 'desc': 'It is really dark down here. And damp. Stairs lead back up into the house.', 'exits': {'u': 0}})
        world.insert(7, { 'visible': False, 'name': 'Tree', 'prefix': 'up a', 'desc': 'You climb to the upper branches of the newly sprouted tree.', 'exits': {'d': 4}})
        world.insert(8, { 'visible': True, 'name': 'Studio', 'prefix': 'in the', 'desc': 'An old painting hangs on the wall of this small space. Another wall has a large print of abstract shapes inside a circle. If you squint, you think the shapes represent something flying out of a tall structure, or they could be a square lollipop barfing feathers. A stairway goes back down to the main room.', 'exits': {'d': 0}})
        world.insert(9, { 'visible': True, 'name': 'Junkyard', 'prefix': 'in the', 'desc': 'The air is thick in this run-down yard. Rusty scrap metal and mismatched tires are strewn about. The exit, back to the street, is on the west end of the junkyard.', 'exits': {'w': 3}})
        world.insert(10, { 'visible': True, 'name': 'Meadow', 'prefix': 'in the', 'desc': 'This grassy spot is pleasant and wide. A lonely stone well sits in the middle. The park is to the west.', 'exits': {'w': 4}})
        world.insert(11, { 'visible': True, 'name': 'Forest path', 'prefix': 'on the', 'desc': 'The dense woods are pierced by a well-worn trail. Looking west, the path appears to open into a dell. To the east, you see the park.', 'exits': {'e':4, 'w': 12}})
        world.insert(12, { 'visible': True, 'name': 'Dell', 'prefix': 'in the', 'desc': 'This gentle valley is surrounded by leafy trees and bushes. A path is visible to the east, and to the north you see a sturdy iron gate that fills the only opening in the foliage.', 'exits': {'e':11} })
        world.insert(13, { 'visible': False, 'name': 'Winding passageway', 'prefix': 'in a', 'desc': 'This jaunty tunnel is dimly lit by bioluminescent lichen. So pretty! The open iron gate is at the south end of the passage. As it bends to the northeast, it goes deeper and deeper into the earth.', 'exits': {'s': 12, 'ne': 14 }})
        world.insert(14, { 'visible': True, 'name': 'Subbasement', 'prefix': 'in the', 'desc': 'This tiny, chilly room opens west to a winding passageway. There\'s a trick one-way trapdoor in the ceiling, which you can access using handholds cut into the wall.', 'exits': {'sw': 13, 'u': 6 }})

        starting_room = 0
        exit_room = 5

        things.append({ 'name': 'note', 'prefix': 'a', 'description': 'Something is badly scrawled on this yellowing paper, but with effort, you can read it. \n\'If you don\'t like it here, exit through the portal.\nObviously, portals aren\'t naturally occuring.\nYou\'ll have to summon one.\nI think there\'s a clue in the studio.\'', 'location': 0, 'on_person': False, 'moveable': True})
        things.append({ 'name': 'pebble', 'prefix': 'a', 'description': 'This tiny rock has been smoothed by eons of natural erosion. How could something so small be so old?', 'location': 1, 'on_person': False, 'moveable': True})
        things.append({ 'name': 'ball', 'prefix': 'a', 'description': 'It\'s a dark pink playground ball.', 'location': 4, 'on_person': False, 'moveable': True})
        things.append({ 'name': 'Mona Lisa', 'prefix': 'the', 'description': 'This painting is a masterpiece of the Italian Renaissance. There is something to that smile.', 'location': 8, 'on_person': False, 'moveable': False})
        things.append({ 'name': 'tricycle', 'prefix': 'a', 'description': 'The light blue aluminum tricycle appears to be in working order, though that plastic seat doesn\'t seem comfortable.', 'location': 3, 'on_person': False, 'moveable': True})
        things.append({ 'name': 'tree kit', 'prefix': 'a', 'description': 'The tree kit box claims: \'Makes a real life tree in seconds! No digging required. For best results, use in an open area.\'', 'location': 2, 'on_person': False, 'moveable': True})
        things.append({ 'name': 'egg', 'prefix': 'an', 'description': 'The small, blue egg feels weighty, like there\'s something inside it.', 'location': 7, 'on_person': False, 'moveable': True})
        things.append({ 'name': 'post', 'prefix': 'a', 'description': 'It\'s four feet tall, stuck in the ground, and has a little square table surface at the top.', 'location': 1, 'on_person': False, 'moveable': False})
        things.append({ 'name': 'machine', 'prefix': 'a', 'description': 'You try to make sense of this large, well-maintained, metallic box. It is the size of a refrigerator but without any visible doors. It has two holes: a small slot near the top and a large square hole at the bottom.', 'location': 9, 'on_person': False, 'moveable': False})
        things.append({ 'name': 'broken well', 'prefix': 'a', 'description': 'It looks like this old well isn\'t completely broken. The crank turns, adjusting the height of the rope, but nothing is attached to it. At the bottom of the well, something reflects light back up to you.', 'location': 10, 'on_person': False, 'moveable': False})
        things.append({ 'name': 'bucket', 'prefix': 'a', 'description': 'This yellow bucket has a wide handle at the top, making it easy to hold.', 'location': 2, 'on_person': False, 'moveable': True})
        things.append({ 'name': 'coin', 'prefix': 'a', 'description': 'This rusty coin has indecipherable symbols on one side and a rectangular shape on the other. It doesn\'t appear to be worth much.', 'location': 13, 'on_person': False, 'moveable': True})
        things.append({ 'name': 'gate', 'prefix': 'a', 'description': 'This is a serious gate. The wrought-iron frame is elegant yet ominous. You see a bulky, brass lock mechanism that contains a happy keyhole.', 'location': 12, 'on_person': False, 'moveable': False})

        #note: if room == 999 then event can be done in any room
        # possible issue: if item can be used in specific room & 999, does room# need to appear before 999 event? why?
        events.insert(0, { 'id': 0, 'done': False, 'room': 8, 'item_name': 'Mona Lisa', 'first_time_text': 'Mona Lisa winks at you.', 'already_done_text': 'The portrait isn\'t doing anything else.' })
        events.insert(1, { 'id': 1, 'done': False, 'room': 0, 'item_name': 'ball', 'first_time_text': 'Mom always said, \'Don\'t play ball in the house.\'', 'already_done_text': 'Seriously, \'Don\'t play ball in the house.\'' })
        events.insert(2, { 'id': 2, 'done': False, 'room': 4, 'item_name': 'tree kit', 'first_time_text': 'Though you can\'t find instructions, the tree kit is suprisingly easy to use. A huge tree shoots up from the earth.', 'already_done_text': 'The kit\'s reagents are all used up.' })
        events.insert(3, { 'id': 3, 'done': False, 'room': 999, 'item_name': 'egg', 'first_time_text': 'You crack open the egg. A slimy robin emerges. It\'s shivering, so you put it in your pocket. The shell falls to your feet.', 'already_done_text': 'It\'s empty. There\'s little to do with the broken egg shell.' })
        events.insert(4, { 'id': 4, 'done': False, 'room': 999, 'item_name': 'tricycle', 'first_time_text': 'You ride the tricycle around and around. Whee!', 'already_done_text': 'You ride the tricycle again. That fun never gets old.' })
        events.insert(5, { 'id': 5, 'done': False, 'room': 6, 'item_name': 'flashlight', 'first_time_text': 'You shine the flashlight across the room. A tiny toy house is now visible on the floor.', 'already_done_text': 'There\'s nothing surprising when you use the flashlight.' })
        events.insert(6, { 'id': 6, 'done': False, 'room': 1, 'item_name': 'toy house', 'first_time_text': 'You attach the toy house to the post. You\'ve made a birdhouse!', 'already_done_text': 'It looks perfect where it is. There\'s nothing more to do with it.' })
        events.insert(7, { 'id': 7, 'done': False, 'room': 1, 'item_name': 'robin', 'first_time_text': 'You place the baby robin into the birdhouse. You hear a loud but pleasant cracking sound in the distance to the east and a little south.', 'already_done_text': 'The bird seems content already. Best leave it alone.' })
        events.insert(8, { 'id': 8, 'done': False, 'room': 8, 'item_name': 'ball', 'first_time_text': 'Mom always said, \'Don\'t play ball in the house.\'', 'already_done_text': 'Seriously, \'Don\'t play ball in the house.\'' })
        events.insert(9, { 'id': 9, 'done': False, 'room': 6, 'item_name': 'ball', 'first_time_text': 'Mom always said, \'Don\'t play ball in the house.\'', 'already_done_text': 'Seriously, \'Don\'t play ball in the house.\'' })
        events.insert(10, { 'id': 10, 'done': False, 'room': 9, 'item_name': 'ball', 'first_time_text': 'You try to fit the ball into the bigger round hole of the machine, but it doesn\'t fit.', 'already_done_text': 'Try as you might, you still can\'t get the ball into the machine.' })
        events.insert(11, { 'id': 11, 'done': False, 'room': 9, 'item_name': 'coin', 'first_time_text': 'You place the coin in the slot of the machine. It pings off metal within, causing gears to churn and grind. It goes silent for a few seconds, then a flashlight shoots out of the lower hole, narrowly missing your leg!', 'already_done_text': 'There\'s nothing more to do with it.' })
        events.insert(12, { 'id': 12, 'done': False, 'room': 999, 'item_name': 'ball', 'first_time_text': 'You throw, catch, and bounce the ball. Fun stuff.', 'already_done_text': 'You throw, catch, and bounce the ball some more. Fun stuff.' })
        events.insert(13, { 'id': 13, 'done': False, 'room': 999, 'item_name': 'note', 'first_time_text': 'Something is badly scrawled on this yellowing paper, but with effort, you can read it. \'If you don\'t like it here, exit through the portal. Obviously, portals aren\'t naturally occuring. You\'ll have to summon one. I think there\'s a clue in the studio.\'', 'already_done_text': 'Something is badly scrawled on this yellowing paper, but with effort, you can read it. \'If you don\'t like it here, exit through the portal. Obviously, portals aren\'t naturally occuring. You\'ll have to summon one. I think there\'s a clue in the studio.\'' })
        events.insert(14, { 'id': 14, 'done': False, 'room': 1, 'item_name': 'post', 'first_time_text': 'The post doesn\'t do anything by itself. Try using another item near it.', 'already_done_text': 'The post doesn\'t do anything by itself. Try using another item near it.' })
        events.insert(15, { 'id': 15, 'done': False, 'room': 9, 'item_name': 'machine', 'first_time_text': 'You can\'t figure out how to get the machine to do anything. Try using another item near it.', 'already_done_text': 'You can\'t figure out how to get the machine to do anything. Try using another item near it.' })
        events.insert(16, { 'id': 16, 'done': False, 'room': 10, 'item_name': 'broken well', 'first_time_text': 'Turning the crank lowers the line into the water and back up again. There\'s definitely something shiny at the bottom of the well, but it\'s too narrow to climb down.', 'already_done_text': 'Turning the crank lowers the line into the water and back up again. There\'s definitely something shiny at the bottom of the well, but it\'s too narrow to climb down.' })
        events.insert(17, { 'id': 17, 'done': False, 'room': 10, 'item_name': 'bucket', 'first_time_text': 'You tie the rope around the bucket handle. You fixed the well!', 'already_done_text': 'Using the bucket now that it is attached doesn\'t do anything. Try something else?' })
        events.insert(18, { 'id': 18, 'done': False, 'room': 10, 'item_name': 'well', 'first_time_text': 'By turning the crank, you lower the bucket into the well. It makes a small splash when it hits the bottom. You raise the bucket from the depths, and you see a moss covered key inside! You grab it, but it slips out of your hand onto the ground.', 'already_done_text': 'You lower and raise the bucket again, but you can\'t fish out anything else from the well.' })
        events.insert(19, { 'id': 19, 'done': False, 'room': 10, 'item_name': 'pebble', 'first_time_text': 'You drop the pebble in the well. It caroms off the stone side then splashes at the bottom. Bloop.', 'already_done_text': 'There\'s nothing more to do with it.' })
        events.insert(20, { 'id': 20, 'done': False, 'room': 12, 'item_name': 'key', 'first_time_text': 'The key glides into the lock! With some effort, you turn the key and pull open the gate. An eerie light is coming from the cave to the north.', 'already_done_text': 'Yep, the key still fits in the lock.' })

        intro_text = 'Well, this is odd. You find yourself in an unfamiliar house.\nYou don\'t remember how you got here. You just know this isn\'t real.\nLook around and use things. If the way forward is not clear, keep looking. And using.\n\nYou must escape and get back to reality!'
        outro_text = 'Congratulations! You escaped that odd world and are back in reality.'


    elif choice == '2':
        world.insert(0, { 'visible': True, 'name': 'Start', 'prefix': 'at the', 'desc': 'This bare room is an octagon. You see a door in the southeast wall.', 'exits': {'se': 1}})
        world.insert(1, { 'visible': True, 'name': 'End', 'prefix': 'at the', 'desc': 'Packed dirt covers the floor of this spacious arena. A door is in the northwest corner. On the south wall, the word "EXIT" is painted in what could be dried blood. Or maybe ketchup? Below it is a large pit. You could probably climb down into it.', 'exits': {'nw': 0, 'd': 2}})
        world.insert(2, { 'visible': True, 'name': 'Exit', 'prefix': 'out the', 'desc': 'End description', 'exits': {}})
        starting_room = 0
        exit_room = 2
        things.append({ 'name': 'hammer', 'prefix': 'a', 'description': 'It\'s a classic ball-peen hammer. Could do some real damage.', 'location': 0, 'on_person': False, 'moveable': True})
        events.insert(0, { 'id': 0, 'done': False, 'room': 999, 'item_name': 'Hammer', 'first_time_text': 'You swing the hammer. If only you had a nail.', 'already_done_text': 'You swing the hammer again.' })
        intro_text = 'This is just a small world to get used to combat.\n\nWhen you get tired of fighting, just drop in the pit.'
        outro_text = 'Welp, you survived. The real challenge lies ahead.'



def initialize_engine():
    global allowed_moves
    global allowed_actions
    global inventory_quantity
    global room_has_items
    global locale_visited
    global available_games
    allowed_moves = ['n', 'north', 's', 'south', 'e', 'east', 'w', 'west', 'u', 'up', 'd', 'down', 'ne', 'northeast', 'nw', 'northwest', 'se', 'southeast', 'sw', 'southwest']
    allowed_actions = ['l', 'look', 'x', 'examine', 'use', 'take', 'drop', 'inv', 'inventory', '?', 'help', 'quit']
    inventory_quantity = 0
    room_has_items = False
    locale_visited = False
    available_games = ['1', '2']

def select_game():
    global available_games
    print('Choose an adventure by number:')
    print('1 - OG Portal')
    print('2 - Combat practice')
    game_choice = input()
    while game_choice not in available_games:
        print('Enter a number from the above list to choose an adventure.')
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
    elif move == 'drop':
        drop_item(room)
    elif move == 'inv' or move == 'inventory':
        show_inventory(inventory_quantity)
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
            room = world[room]['exits'][dir]
            locale_visited = False
        else:
            print('You can\'t go that way.')
    print ('')

if room == exit_room:
    print(outro_text)
    print('')
    input('Press ENTER to continue...')
