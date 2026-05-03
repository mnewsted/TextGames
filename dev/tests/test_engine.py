import pytest
from unittest.mock import MagicMock
from engine import extract_target, short_move, valid_move


class TestExtractTarget:
    def _make_state(self):
        state = MagicMock()
        state.choice = ''
        return state

    def test_verb_only(self):
        state = self._make_state()
        target = extract_target('look', state)
        assert target == ''
        assert state.choice == 'look'

    def test_verb_and_noun(self):
        state = self._make_state()
        target = extract_target('use elixir', state)
        assert target == 'elixir'
        assert state.choice == 'use'

    def test_verb_and_multiword_noun(self):
        state = self._make_state()
        target = extract_target('use magic key', state)
        assert target == 'magic key'
        assert state.choice == 'use'

    def test_choice_always_set_for_single_word(self):
        state = self._make_state()
        extract_target('take', state)
        assert state.choice == 'take'


class TestShortMove:
    def test_single_letter_unchanged(self):
        assert short_move('n') == 'n'

    def test_full_cardinal_truncated(self):
        assert short_move('north') == 'n'
        assert short_move('south') == 's'
        assert short_move('east') == 'e'
        assert short_move('west') == 'w'
        assert short_move('down') == 'd'

    def test_up_special_case(self):
        assert short_move('up') == 'u'

    def test_diagonal_abbreviated(self):
        assert short_move('northeast') == 'ne'
        assert short_move('northwest') == 'nw'
        assert short_move('southeast') == 'se'
        assert short_move('southwest') == 'sw'

    def test_two_letter_unchanged(self):
        assert short_move('ne') == 'ne'


class TestValidMove:
    def _make_state(self, exits):
        state = MagicMock()
        state.world = [{
            'exits': exits,
            'visible': True, 'name': 'Room', 'prefix': 'in', 'name2': '', 'desc': '',
        }]
        return state

    def test_valid_direction(self):
        state = self._make_state({'n': 0, 's': 0})
        assert valid_move(0, 'n', state) is True

    def test_invalid_direction(self):
        state = self._make_state({'n': 0})
        assert valid_move(0, 's', state) is False

    def test_empty_exits(self):
        state = self._make_state({})
        assert valid_move(0, 'n', state) is False
