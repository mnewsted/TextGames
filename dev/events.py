"""
Event dispatch: check_event finds the right event for a used item and delegates
to the active world module's handle_event(). do_special delegates room-entry
logic to handle_special().

do_event() from games.py is NOT here — it lives inside each world module as
handle_event(event_id, current_room, state).

do_multi_step_event() is gone — its logic is inlined into world4.handle_event().
code_checker() is gone — it is the _code_checker() helper inside world3.
"""


def check_event(item_name, current_room, state, world_module):
    """Find and dispatch the first event that matches item_name in current_room.

    Matching rules:
      - event['item_name'] must equal item_name (case-insensitive)
      - event['room'] must equal current_room OR be 999 (anywhere)

    Events are stored in list order with room-specific entries *before* their
    room=999 counterparts for the same item, so a plain linear search always
    finds the most specific match first.

    Returns True if a matching event was found (fired or already done),
    False if no event exists for this item/room combination.
    """
    name_lower = item_name.lower()
    for event_id, event in enumerate(state.events):
        if event['item_name'].lower() != name_lower:
            continue
        if event['room'] != 999 and event['room'] != current_room:
            continue
        # Matching event found — either fire it or report already done
        if event['done']:
            print(event['already_done_text'])
        else:
            world_module.handle_event(event_id, current_room, state)
        return True
    return False


def do_special(current_room, state, world_module):
    """Run room-entry special logic by delegating to the world module.

    Called from locale() whenever current_room is in state.special_rooms.
    Each world's handle_special() decides what actually happens (bad air,
    turtle transformation, ambient lake flavour, captain monologue, etc.).
    """
    world_module.handle_special(current_room, state)
