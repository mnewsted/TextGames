import pytest
from unittest.mock import MagicMock
from combat import creature_wellness, player_wellness


class TestCreatureWellness:
    def test_full_health(self):
        assert 'good shape' in creature_wellness(100, 100)

    def test_above_75(self):
        assert 'good shape' in creature_wellness(80, 100)

    def test_above_50(self):
        assert 'some pain' in creature_wellness(60, 100)

    def test_above_25(self):
        assert 'hurting' in creature_wellness(30, 100)

    def test_near_death(self):
        assert 'seriously wounded' in creature_wellness(10, 100)

    def test_dead(self):
        assert creature_wellness(0, 100) == 'is dead.'

    def test_includes_hp_suffix(self):
        result = creature_wellness(60, 100)
        assert '(60/100)' in result

    def test_zero_max_hp(self):
        # Should not raise ZeroDivisionError
        result = creature_wellness(0, 0)
        assert 'dead' in result


class TestPlayerWellness:
    def _make_state(self, hp):
        state = MagicMock()
        state.player_hp = hp
        return state

    def test_good_shape(self, capsys):
        player_wellness(self._make_state(90))
        assert 'good shape' in capsys.readouterr().out

    def test_some_pain(self, capsys):
        player_wellness(self._make_state(60))
        assert 'some pain' in capsys.readouterr().out

    def test_hurting(self, capsys):
        player_wellness(self._make_state(30))
        assert 'hurting' in capsys.readouterr().out

    def test_seriously_wounded(self, capsys):
        player_wellness(self._make_state(10))
        assert 'seriously wounded' in capsys.readouterr().out

    def test_dead(self, capsys):
        player_wellness(self._make_state(0))
        assert 'dead' in capsys.readouterr().out

    def test_includes_hp_suffix(self, capsys):
        player_wellness(self._make_state(75))
        assert '(75/100)' in capsys.readouterr().out
