import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pytest
from corp_game.game import Game


def setup_game():
    g = Game()
    g.add_player('Alice')
    g.add_player('Bob')
    g.submit_word('Alice', 'apple')
    g.submit_word('Bob', 'banana')
    g.start()
    return g


def test_correct_guess():
    g = setup_game()
    assert g.guess('Alice', 'Bob', 'banana') is True
    state = g.state()
    assert state['ceo'] == 'Alice'
    assert 'Bob' in state['employees']['Alice']


def test_wrong_guess():
    g = setup_game()
    assert g.guess('Alice', 'Bob', 'apple') is False
    state = g.state()
    assert state['ceo'] == 'Bob'
