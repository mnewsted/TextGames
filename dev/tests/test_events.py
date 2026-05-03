import pytest
from unittest.mock import MagicMock, call
from events import check_event


def _make_state(events):
    state = MagicMock()
    state.events = events
    return state


def _event(item_name, room, done=False, first='first text', already='already text'):
    return {
        'item_name': item_name,
        'room': room,
        'done': done,
        'first_time_text': first,
        'already_done_text': already,
    }


class TestCheckEvent:
    def test_fires_in_matching_room(self):
        state = _make_state([_event('elixir', 1)])
        world = MagicMock()
        result = check_event('elixir', 1, state, world)
        assert result is True
        world.handle_event.assert_called_once_with(0, 1, state)

    def test_room_999_fires_anywhere(self):
        state = _make_state([_event('hammer', 999)])
        world = MagicMock()
        result = check_event('hammer', 5, state, world)
        assert result is True
        world.handle_event.assert_called_once()

    def test_wrong_room_returns_false(self):
        state = _make_state([_event('elixir', 1)])
        world = MagicMock()
        result = check_event('elixir', 0, state, world)
        assert result is False
        world.handle_event.assert_not_called()

    def test_no_matching_item_returns_false(self):
        state = _make_state([_event('hammer', 999)])
        world = MagicMock()
        result = check_event('elixir', 0, state, world)
        assert result is False

    def test_already_done_prints_text_returns_true(self, capsys):
        state = _make_state([_event('elixir', 999, done=True, already='Already done.')])
        world = MagicMock()
        result = check_event('elixir', 0, state, world)
        assert result is True
        world.handle_event.assert_not_called()
        assert 'Already done.' in capsys.readouterr().out

    def test_case_insensitive_item_name(self):
        state = _make_state([_event('Magic Key', 999)])
        world = MagicMock()
        result = check_event('magic key', 0, state, world)
        assert result is True

    def test_specific_room_match_before_999(self):
        # Room-specific event should fire before the room=999 fallback
        events = [
            _event('key', 1, first='room-specific'),
            _event('key', 999, first='anywhere'),
        ]
        state = _make_state(events)
        world = MagicMock()
        check_event('key', 1, state, world)
        world.handle_event.assert_called_once_with(0, 1, state)
