"""
GameState — holds all mutable game data that currently lives as globals in games.py.

Every module receives a GameState instance instead of reading/writing globals.
This also makes save/load trivial: serialize one object rather than 18+ variables.

Populated in step 2 of the refactor (replace globals).
"""

import copy
from worlds import load_world as _load_world_module


class GameState:
    def __init__(self):
        # --- World identity ---
        self.game_choice = ''

        # --- Room / world data (deep-copied from world module on load) ---
        self.world = []          # list of room dicts
        self.things = []         # list of item dicts
        self.creatures = []      # list of creature dicts
        self.events = []         # list of event dicts

        # --- World constants (set from world module on load) ---
        self.starting_room = 0
        self.exit_room = 0
        self.safe_rooms = []
        self.special_rooms = []
        self.special_done = []
        self.intro_text = ''
        self.outro_text = ''

        # --- Navigation state ---
        self.room = 0

        # --- Player state ---
        self.player_hp = 100
        self.inventory_quantity = 0  # count of items with on_person == True

        # --- Turn-level cache ---
        self.locale_visited = False  # True if room was already printed this turn

        # --- Input / move tracking ---
        self.move = ''
        self.last_move = ''
        self.choice = ''
        self.target = ''

        # --- Display settings ---
        self.verbose_mode = True   # show exits on first visit when True

        # --- World-specific state ---
        self.launch_code = ''      # used by world 3 (Space Adventure)

    # ------------------------------------------------------------------
    # World loading
    # ------------------------------------------------------------------

    def load_world(self, game_choice):
        """Deep-copy all world-module data into state and reset per-game variables."""
        mod = _load_world_module(game_choice)

        self.game_choice = game_choice
        self.world = copy.deepcopy(mod.ROOMS)
        self.things = copy.deepcopy(mod.ITEMS)
        self.creatures = copy.deepcopy(mod.CREATURES)
        self.events = copy.deepcopy(mod.EVENTS)

        self.starting_room = mod.STARTING_ROOM
        self.exit_room = mod.EXIT_ROOM
        self.safe_rooms = list(mod.SAFE_ROOMS)
        self.special_rooms = list(mod.SPECIAL_ROOMS)
        self.special_done = copy.deepcopy(mod.SPECIAL_DONE)
        self.intro_text = mod.INTRO_TEXT
        self.outro_text = mod.OUTRO_TEXT

        self.room = mod.STARTING_ROOM
        self.player_hp = 100
        self.inventory_quantity = 0
        self.launch_code = getattr(mod, 'LAUNCH_CODE', '')

        # Reset turn-level state
        self.locale_visited = False
        self.move = ''
        self.last_move = ''
        self.choice = ''
        self.target = ''

    # ------------------------------------------------------------------
    # Item helpers
    # ------------------------------------------------------------------

    def add_thing(self, item_dict):
        """Append item to things; increment inventory_quantity if on_person."""
        self.things.append(item_dict)
        if item_dict.get('on_person'):
            self.inventory_quantity += 1

    def delete_thing(self, name):
        """Remove the first item whose name matches (case-insensitive).

        Decrements inventory_quantity if the removed item was on_person.
        """
        for i, thing in enumerate(self.things):
            if thing['name'].lower() == name.lower():
                if thing.get('on_person'):
                    self.inventory_quantity -= 1
                self.things.pop(i)
                return

    # ------------------------------------------------------------------
    # Computed room state
    # ------------------------------------------------------------------

    @property
    def room_has_items(self) -> bool:
        return any(t['location'] == self.room and not t['on_person'] for t in self.things)

    @property
    def room_has_mobs(self) -> bool:
        return any(not c['is_dead'] and c['room'] == self.room for c in self.creatures)
