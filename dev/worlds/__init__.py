"""
World loader. Returns the correct world module for the selected game.

Usage (from engine or main):
    world = load_world(state.game_choice)
    world.handle_event(event_id, state)
"""

from worlds import world1, world2, world3, world4

_WORLDS = {
    '1': world1,
    '2': world2,
    '3': world3,
    '4': world4,
}


def load_world(game_choice):
    """Return the world module for the given game choice string ('1'–'4')."""
    return _WORLDS[game_choice]
