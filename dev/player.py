"""
OOP entity definitions: Player class + dataclasses for Room, Item, Event, Creature.

These are the *target shapes* for step 6 (full module split). World modules
currently produce plain dicts; each dataclass has a from_dict() factory so
the conversion can happen incrementally without rewriting all four world modules
at once.

Populated in step 3 of the refactor (OOP entities).
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------

class Player:
    """Tracks player health. Replaces the player_hp global and the
    player_wellness() display function in games.py."""

    MAX_HP = 100

    def __init__(self, hp: int = 100):
        self.hp = hp

    def heal(self, amount: int) -> None:
        self.hp = min(self.hp + amount, self.MAX_HP)

    def take_damage(self, amount: int) -> None:
        self.hp = max(self.hp - amount, 0)

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def wellness_label(self) -> str:
        """Return a short phrase describing current health (mirrors player_wellness in games.py)."""
        pct = self.hp / self.MAX_HP
        if pct == 1.0:
            return 'You feel great!'
        if pct >= 0.75:
            return 'You feel good.'
        if pct >= 0.50:
            return 'You feel okay.'
        if pct >= 0.25:
            return 'You are hurting.'
        return 'You are in bad shape!'


# ---------------------------------------------------------------------------
# Room
# ---------------------------------------------------------------------------

@dataclass
class Room:
    visible: bool
    name: str
    prefix: str
    name2: str
    desc: str
    exits: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> 'Room':
        return cls(
            visible=d['visible'],
            name=d['name'],
            prefix=d['prefix'],
            name2=d['name2'],
            desc=d['desc'],
            exits=dict(d.get('exits', {})),
        )

    def to_dict(self) -> dict:
        return {
            'visible': self.visible,
            'name': self.name,
            'prefix': self.prefix,
            'name2': self.name2,
            'desc': self.desc,
            'exits': dict(self.exits),
        }


# ---------------------------------------------------------------------------
# Item
# ---------------------------------------------------------------------------

@dataclass
class Item:
    name: str
    prefix: str
    description: str
    location: int
    on_person: bool
    moveable: bool
    is_weapon: bool
    no_drop: bool
    base_damage: int = 0
    damage: int = 0
    hit_bonus: int = 0

    @classmethod
    def from_dict(cls, d: dict) -> 'Item':
        return cls(
            name=d['name'],
            prefix=d['prefix'],
            description=d['description'],
            location=d['location'],
            on_person=d['on_person'],
            moveable=d['moveable'],
            is_weapon=d['is_weapon'],
            no_drop=d['no_drop'],
            base_damage=d.get('base_damage', 0),
            damage=d.get('damage', 0),
            hit_bonus=d.get('hit_bonus', 0),
        )

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'prefix': self.prefix,
            'description': self.description,
            'location': self.location,
            'on_person': self.on_person,
            'moveable': self.moveable,
            'is_weapon': self.is_weapon,
            'no_drop': self.no_drop,
            'base_damage': self.base_damage,
            'damage': self.damage,
            'hit_bonus': self.hit_bonus,
        }


# ---------------------------------------------------------------------------
# Event
# ---------------------------------------------------------------------------

@dataclass
class Event:
    id: int
    done: bool
    room: int        # 999 = usable anywhere
    item_name: str
    first_time_text: str
    already_done_text: str

    @classmethod
    def from_dict(cls, d: dict) -> 'Event':
        return cls(
            id=d['id'],
            done=d['done'],
            room=d['room'],
            item_name=d['item_name'],
            first_time_text=d['first_time_text'],
            already_done_text=d['already_done_text'],
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'done': self.done,
            'room': self.room,
            'item_name': self.item_name,
            'first_time_text': self.first_time_text,
            'already_done_text': self.already_done_text,
        }


# ---------------------------------------------------------------------------
# Creature
# ---------------------------------------------------------------------------

@dataclass
class Creature:
    id: int
    name: str
    description: str
    room: int
    max_hp: int
    current_hp: int
    is_dead: bool
    is_hostile: bool
    status_neutral: str
    status_hostile: str
    damage: int
    hit_bonus: int
    attack_chance: int
    is_fatigued: bool
    death_event: int
    was_seen: bool
    dead_description: str

    @property
    def is_alive(self) -> bool:
        return not self.is_dead

    def wellness_label(self) -> str:
        """Return a short phrase describing creature health (mirrors creature_wellness in games.py)."""
        pct = self.current_hp / self.max_hp if self.max_hp else 0
        if pct == 1.0:
            return 'looks uninjured.'
        if pct >= 0.75:
            return 'looks lightly injured.'
        if pct >= 0.50:
            return 'looks moderately injured.'
        if pct >= 0.25:
            return 'looks badly injured.'
        return 'looks near death.'

    @classmethod
    def from_dict(cls, d: dict) -> 'Creature':
        return cls(
            id=d['id'],
            name=d['name'],
            description=d['description'],
            room=d['room'],
            max_hp=d['max_hp'],
            current_hp=d['current_hp'],
            is_dead=d['is_dead'],
            is_hostile=d['is_hostile'],
            status_neutral=d['status_neutral'],
            status_hostile=d['status_hostile'],
            damage=d['damage'],
            hit_bonus=d['hit_bonus'],
            attack_chance=d['attack_chance'],
            is_fatigued=d['is_fatigued'],
            death_event=d['death_event'],
            was_seen=d['was_seen'],
            dead_description=d['dead_description'],
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'room': self.room,
            'max_hp': self.max_hp,
            'current_hp': self.current_hp,
            'is_dead': self.is_dead,
            'is_hostile': self.is_hostile,
            'status_neutral': self.status_neutral,
            'status_hostile': self.status_hostile,
            'damage': self.damage,
            'hit_bonus': self.hit_bonus,
            'attack_chance': self.attack_chance,
            'is_fatigued': self.is_fatigued,
            'death_event': self.death_event,
            'was_seen': self.was_seen,
            'dead_description': self.dead_description,
        }
