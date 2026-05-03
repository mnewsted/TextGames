"""
Save/load: serialize GameState to a base64-encoded JSON file and restore it.

room_has_items and room_has_mobs are computed @property methods in GameState
and are NOT persisted — they reconstruct themselves from state.things/creatures.
"""

import base64
import datetime
import json


def save_game(state):
    if check_for_saved_games('save', state.game_choice):
        print('Are you sure you want to save your current progress and overwrite this earlier saved game?')
    else:
        print('Are you sure you want to save your progress?')
    confirm = input()
    if confirm.lower() not in ('y', 'yes'):
        print('Okay, back to it.')
        return
    print('We will keep track of which game # you are playing and the time you saved.')
    note = input('Enter a note about your progress: ')
    save_time = datetime.datetime.now().strftime("%B %d, %Y at %H:%M:%S %p")
    print(try_save_game(state, save_time, note))


def load_saved_game(state):
    """Load a saved game into state. Returns True if load succeeded."""
    if not check_for_saved_games('load', state.game_choice):
        return False
    print('Are you sure you want to overwrite your current progress with this saved game?')
    confirm = input()
    if confirm.lower() not in ('y', 'yes'):
        print('Okay, back to it.')
        return False
    msg = try_load_saved_game(state)
    print(msg)
    return msg.startswith('Game loaded')


def check_for_saved_games(action, game):
    filename = 'saved_game' + game + '.sav'
    try:
        with open(filename, 'r') as f:
            raw = f.read()
        saved = json.loads(base64.b64decode(raw))
    except FileNotFoundError:
        if action == 'save':
            return False
        print('Sorry. Saved game progress not found.')
        return False
    except Exception:
        return False

    label = (f"Game # {saved['saved_game_choice']} on {saved['saved_game_time']}"
             f" with note: {saved['saved_game_note']}")
    if action == 'save':
        print('WARNING: This will overwrite your saved game progress.')
        print(f'We found this saved game progress: {label}')
        return True
    print('WARNING: Loading a game will overwrite your current progress.')
    print(f'We found this saved game progress: {label}')
    return True


def try_save_game(state, save_time, note):
    filename = 'saved_game' + state.game_choice + '.sav'
    payload = {
        'saved_game_choice':        state.game_choice,
        'saved_game_time':          save_time,
        'saved_game_note':          note,
        'saved_things':             state.things,
        'saved_world':              state.world,
        'saved_events':             state.events,
        'saved_room':               state.room,
        'saved_last_move':          state.last_move,
        'saved_player_hp':          state.player_hp,
        'saved_creatures':          state.creatures,
        'saved_inventory_quantity': state.inventory_quantity,
        'saved_special_done':       state.special_done,
        'saved_safe_rooms':         state.safe_rooms,
        'saved_launch_code':        state.launch_code,
        'saved_exit_room':          state.exit_room,
        'saved_intro_text':         state.intro_text,
        'saved_outro_text':         state.outro_text,
        'saved_locale_visited':     state.locale_visited,
        'saved_special_rooms':      state.special_rooms,
        'saved_verbose_mode':       state.verbose_mode,
    }
    encoded = base64.b64encode(json.dumps(payload).encode('utf-8'))
    try:
        with open(filename, 'wb') as f:
            f.write(encoded)
    except FileNotFoundError:
        return 'Sorry. We could not save your game. Contact Tech Support.\n'
    return f'Saved: Game # {state.game_choice} on {save_time} with note: {note}'


def try_load_saved_game(state):
    filename = 'saved_game' + state.game_choice + '.sav'
    try:
        with open(filename, 'r') as f:
            raw = f.read()
        saved = json.loads(base64.b64decode(raw))
    except FileNotFoundError:
        return 'Sorry. We could not load your game. Contact Tech Support.\n'

    state.things             = saved['saved_things']
    state.world              = saved['saved_world']
    state.events             = saved['saved_events']
    state.room               = saved['saved_room']
    state.last_move          = saved['saved_last_move']
    state.player_hp          = saved['saved_player_hp']
    state.creatures          = saved['saved_creatures']
    state.inventory_quantity = saved['saved_inventory_quantity']
    state.special_done       = saved['saved_special_done']
    state.safe_rooms         = saved['saved_safe_rooms']
    state.launch_code        = saved['saved_launch_code']
    state.exit_room          = saved['saved_exit_room']
    state.intro_text         = saved['saved_intro_text']
    state.outro_text         = saved['saved_outro_text']
    state.locale_visited     = saved['saved_locale_visited']
    state.special_rooms      = saved['saved_special_rooms']
    state.verbose_mode       = saved['saved_verbose_mode']
    return 'Game loaded!\n'
