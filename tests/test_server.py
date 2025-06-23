import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from corp_game.server import create_app, GAME
import json

app = create_app()

def setup_module():
    # reset game for tests
    GAME.players.clear()
    GAME.words.clear()
    GAME.employees.clear()
    GAME.ceo = None
    GAME.started = False


def test_endpoints():
    with app.test_client() as c:
        # add players
        c.post('/players', json={'name': 'Alice'})
        c.post('/players', json={'name': 'Bob'})
        # submit words
        c.post('/submit-word', json={'name': 'Alice', 'word': 'apple'})
        c.post('/submit-word', json={'name': 'Bob', 'word': 'banana'})
        # start game
        rv = c.post('/start')
        data = rv.get_json()
        assert set(data['words']) == {'apple', 'banana'}
        # correct guess
        rv = c.post('/guess', json={'guesser': 'Alice', 'target': 'Bob', 'word': 'banana'})
        assert rv.get_json()['correct'] is True
        rv = c.get('/state')
        state = rv.get_json()
        assert state['ceo'] == 'Alice'
