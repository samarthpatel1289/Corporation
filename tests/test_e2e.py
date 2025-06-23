import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import requests
import threading
import time
from corp_game.server import app, GAME


def run_app():
    app.run(port=5001)


def setup_module(module):
    # reset game state
    GAME.players.clear()
    GAME.words.clear()
    GAME.employees.clear()
    GAME.ceo = None
    GAME.started = False
    # start server thread
    module.server = threading.Thread(target=run_app, daemon=True)
    module.server.start()
    time.sleep(1)


def teardown_module(module):
    # Flask dev server stops when main thread exits
    pass


def test_flow():
    url = 'http://localhost:5001'
    requests.post(f'{url}/players', json={'name': 'Alice'})
    requests.post(f'{url}/players', json={'name': 'Bob'})
    requests.post(f'{url}/submit-word', json={'name': 'Alice', 'word': 'apple'})
    requests.post(f'{url}/submit-word', json={'name': 'Bob', 'word': 'banana'})
    r = requests.post(f'{url}/start')
    assert set(r.json()['words']) == {'apple', 'banana'}
    r = requests.post(f'{url}/guess', json={'guesser': 'Alice', 'target': 'Bob', 'word': 'banana'})
    assert r.json()['correct'] is True
    r = requests.get(f'{url}/state')
    assert r.json()['ceo'] == 'Alice'
