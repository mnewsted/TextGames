import pytest
from state import GameState


def _item(name, location, on_person=False):
    return {
        'name': name, 'prefix': 'a', 'description': '',
        'location': location, 'on_person': on_person,
        'moveable': True, 'is_weapon': False, 'no_drop': False,
    }


def _creature(room, is_dead=False):
    return {
        'id': 0, 'name': 'Mob', 'description': '', 'room': room,
        'max_hp': 100, 'current_hp': 100, 'is_dead': is_dead,
        'is_hostile': False, 'status_neutral': '', 'status_hostile': '',
        'damage': 10, 'hit_bonus': 0, 'attack_chance': 50,
        'is_fatigued': False, 'death_event': 0, 'was_seen': False,
        'dead_description': '',
    }


class TestRoomHasItems:
    def setup_method(self):
        self.state = GameState()
        self.state.room = 0

    def test_item_in_room_not_carried(self):
        self.state.things = [_item('hammer', 0)]
        assert self.state.room_has_items is True

    def test_item_in_room_but_carried(self):
        self.state.things = [_item('hammer', 0, on_person=True)]
        assert self.state.room_has_items is False

    def test_item_in_different_room(self):
        self.state.things = [_item('hammer', 1)]
        assert self.state.room_has_items is False

    def test_no_items(self):
        self.state.things = []
        assert self.state.room_has_items is False

    def test_mixed_items(self):
        self.state.things = [
            _item('carried', 0, on_person=True),
            _item('on_floor', 0, on_person=False),
        ]
        assert self.state.room_has_items is True


class TestRoomHasMobs:
    def setup_method(self):
        self.state = GameState()
        self.state.room = 0

    def test_live_mob_in_room(self):
        self.state.creatures = [_creature(0)]
        assert self.state.room_has_mobs is True

    def test_dead_mob_in_room(self):
        self.state.creatures = [_creature(0, is_dead=True)]
        assert self.state.room_has_mobs is False

    def test_mob_in_different_room(self):
        self.state.creatures = [_creature(1)]
        assert self.state.room_has_mobs is False

    def test_no_creatures(self):
        self.state.creatures = []
        assert self.state.room_has_mobs is False


class TestAddDeleteThing:
    def setup_method(self):
        self.state = GameState()
        self.state.things = [_item('hammer', 0)]

    def test_delete_existing(self):
        self.state.delete_thing('hammer')
        assert all(t['name'] != 'hammer' for t in self.state.things)

    def test_delete_nonexistent_is_safe(self):
        self.state.delete_thing('ghost item')
        assert len(self.state.things) == 1

    def test_add_thing(self):
        new_item = _item('elixir', 0)
        self.state.add_thing(new_item)
        assert any(t['name'] == 'elixir' for t in self.state.things)
