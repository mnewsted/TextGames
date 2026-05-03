"""
Combat system: attack logic, creature reactions, fatigue, following, and
the two wellness display helpers used by both engine and combat functions.

player_wellness / creature_wellness live here (not engine.py) so that
engine.py can import from combat without creating a circular dependency.
"""

import random


# ---------------------------------------------------------------------------
# Wellness display helpers
# ---------------------------------------------------------------------------

def creature_wellness(current_hp, max_hp):
    pct = (current_hp / max_hp * 100) if max_hp else 0
    suffix = f' ({current_hp}/{max_hp})'
    if pct > 75:
        return 'is in good shape.' + suffix
    if pct > 50:
        return 'appears to be in some pain.' + suffix
    if pct > 25:
        return 'is hurting but still dangerous.' + suffix
    if pct > 0:
        return 'is seriously wounded.' + suffix
    return 'is dead.'


def player_wellness(state):
    current = state.player_hp
    suffix = f' ({current}/100)'
    if current > 75:
        print('You are in good shape.' + suffix)
    elif current > 50:
        print('You are in some pain.' + suffix)
    elif current > 25:
        print('You are hurting but still able to fight.' + suffix)
    elif current > 0:
        print('You are seriously wounded.' + suffix)
    else:
        print('You are dead.')


# ---------------------------------------------------------------------------
# Weapon / defense helpers
# ---------------------------------------------------------------------------

def weapon_checker(item_name, state):
    for thing in state.things:
        if thing['name'].lower() == item_name.lower():
            return thing['is_weapon']
    return False


def defense_checker(item_name, state):
    return state.game_choice == '4' and item_name.lower() == 'shell'


def pick_up_if_weapon(item_name, state):
    """Auto-pick-up a weapon before combat if it isn't already carried."""
    for thing in state.things:
        if thing['name'].lower() == item_name.lower() and thing['is_weapon']:
            if not thing['on_person']:
                thing['on_person'] = True
                state.inventory_quantity += 1
                print('You pick up the ' + thing['name'] + '.')
            return


def creature_in_same_room(creature_id, current_room, state):
    mob = state.creatures[creature_id]
    return not mob['is_dead'] and mob['room'] == current_room


# ---------------------------------------------------------------------------
# Attack helpers
# ---------------------------------------------------------------------------

def attack_checker(current_room, state):
    """Ask the player whether to attack a neutral mob. Returns True to proceed."""
    if not state.room_has_mobs:
        return False
    for mob in state.creatures:
        if mob['room'] == current_room and not mob['is_dead']:
            if not mob['is_hostile']:
                print('Do you want to attack ' + mob['name'] + '? This will make it hostile towards you.')
                answer = input("Enter 'Y' or 'Yes': ")
                return answer.lower() in ('y', 'yes')
            return True  # already hostile — player confirmed by using a weapon
    return False


# ---------------------------------------------------------------------------
# Combat actions
# ---------------------------------------------------------------------------

def player_attack(current_room, weapon_name, state, world_module):
    if not state.room_has_mobs:
        return
    for mob in state.creatures:
        if mob['room'] != current_room or mob['is_dead']:
            continue

        # Find the weapon item; bail if it isn't actually a weapon
        weapon_thing = next(
            (t for t in state.things if t['name'].lower() == weapon_name.lower()),
            None,
        )
        if weapon_thing is None or not weapon_thing['is_weapon']:
            return

        mob['is_hostile'] = True
        if current_room in state.special_rooms:
            world_module.handle_special(current_room, state)

        if (random.randrange(0, 100) + weapon_thing['hit_bonus']) > 50:
            damage = weapon_thing['base_damage'] + random.randrange(0, weapon_thing['damage'] + 1)
            verb = 'They hit' if weapon_name.endswith('s') else 'It hits'
            print(f'{verb} {mob["name"]} for {damage} damage.')
            mob['current_hp'] -= damage
            if mob['current_hp'] <= 0:
                print('That was a fatal blow.')
                mob['is_dead'] = True
        else:
            miss = random.randrange(1, 11)
            if miss < 6:
                verb = 'They miss' if weapon_name.endswith('s') else 'It misses'
                print(f'{verb} {mob["name"]}.')
            elif miss < 9:
                print(mob['name'] + ' dodges the attack.')
            else:
                print('The attack glances off ' + mob['name'] + '.')

        print(mob['name'] + ' ' + creature_wellness(mob['current_hp'], mob['max_hp']))
        if mob['is_dead']:
            if mob['death_event'] != 0:
                world_module.handle_event(mob['death_event'], current_room, state)
        else:
            print('')
        return  # one mob per attack call


def creature_attack(current_room, state):
    if not state.room_has_mobs:
        return
    for mob in state.creatures:
        if mob['room'] != current_room or mob['is_dead'] or not mob['is_hostile']:
            continue
        if not mob['is_fatigued'] and mob['attack_chance'] >= random.randrange(1, 101):
            print(mob['name'] + ' attacks!')
            mob['is_fatigued'] = True
            if (random.randrange(1, 101) + mob['hit_bonus']) > 50:
                damage = 10 + random.randrange(0, mob['damage'] + 1)
                print('It hits you for ' + str(damage) + ' damage.')
                state.player_hp -= damage
                if state.player_hp <= 0:
                    print('That was a fatal blow.')
            else:
                miss = random.randrange(1, 11)
                if miss < 6:
                    print('It misses you.')
                elif miss < 9:
                    print('You dodge the attack.')
                else:
                    print('The attack glances off you.')
        else:
            posture = random.randrange(1, 4)
            if posture == 1:
                print(mob['name'] + ' gives you a hateful stare.')
            elif posture == 2:
                print(mob['name'] + ' catches its breath.')
            else:
                print(mob['name'] + ' readies for combat.')
        player_wellness(state)


def creature_attack_block(current_room, state, world_module):
    """Shell-defence variant: damage may be blocked, reflected, or converted."""
    if not state.room_has_mobs:
        return
    for mob in state.creatures:
        if mob['room'] != current_room or mob['is_dead'] or not mob['is_hostile']:
            continue
        if not mob['is_fatigued'] and mob['attack_chance'] >= random.randrange(1, 101):
            print('\n' + mob['name'] + ' attacks!')
            mob['is_fatigued'] = True
            if (random.randrange(1, 101) + mob['hit_bonus']) > 50:
                block_type = random.randrange(1, 101)
                if block_type <= 25:
                    print('Your shell blocks all damage.')
                elif block_type <= 50:
                    print('Your shell absorbs the attack and converts part of it into health.')
                    state.player_hp = min(state.player_hp + random.randrange(1, 4), 100)
                elif block_type <= 75:
                    print('The assault is partly lessened by your shell.')
                    damage = int((6 + random.randrange(0, mob['damage'] + 1)) / 2)
                    print('It hits you for ' + str(damage) + ' damage.')
                    state.player_hp -= damage
                    if state.player_hp <= 0:
                        print('That was a fatal blow.')
                else:
                    print('Your shell deflects the attack back onto your enemy.')
                    damage = int((10 + random.randrange(0, mob['damage'] + 1)) / 4)
                    print('It hits ' + mob['name'] + ' for ' + str(damage) + ' damage.')
                    mob['current_hp'] -= damage
                    if mob['current_hp'] <= 0:
                        print('That was a fatal blow.')
                        mob['is_dead'] = True
                    print(mob['name'] + ' ' + creature_wellness(mob['current_hp'], mob['max_hp']))
                    if mob['is_dead'] and mob['death_event'] != 0:
                        world_module.handle_event(mob['death_event'], current_room, state)
                    elif not mob['is_dead']:
                        print('')
            else:
                miss = random.randrange(1, 11)
                if miss < 6:
                    print('It misses you.')
                elif miss < 9:
                    print('You dodge the attack.')
                else:
                    print('The attack glances off you.')
        else:
            posture = random.randrange(1, 4)
            if posture == 1:
                print(mob['name'] + ' gives you a hateful stare.')
            elif posture == 2:
                print(mob['name'] + ' catches its breath.')
            else:
                print(mob['name'] + ' readies for combat.')
        if not mob['is_dead']:
            player_wellness(state)


# ---------------------------------------------------------------------------
# Movement / fatigue
# ---------------------------------------------------------------------------

def creature_follow(current_room, new_room, state):
    if new_room in state.safe_rooms or new_room == state.exit_room:
        return
    if state.room_has_mobs:
        for mob in state.creatures:
            if mob['room'] == current_room and not mob['is_dead'] and mob['is_hostile']:
                mob['room'] = new_room
                print(mob['name'] + ' follows you.')


def remove_creature_fatigue(current_room, state):
    if state.room_has_mobs:
        for mob in state.creatures:
            if mob['room'] == current_room and not mob['is_dead'] and mob['is_hostile']:
                mob['is_fatigued'] = False
