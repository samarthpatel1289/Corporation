from flask import Flask, render_template, jsonify, request
from .game import Game

app = Flask(__name__)
GAME = Game()
@app.get("/")
def index():
    return render_template("index.html")



@app.post('/players')
def add_player():
    data = request.get_json()
    GAME.add_player(data['name'])
    return jsonify({'status': 'ok'})


@app.post('/submit-word')
def submit_word():
    data = request.get_json()
    GAME.submit_word(data['name'], data['word'])
    return jsonify({'status': 'ok'})


@app.post('/start')
def start():
    words = GAME.start()
    return jsonify({'words': words})


@app.post('/guess')
def guess():
    data = request.get_json()
    result = GAME.guess(data['guesser'], data['target'], data['word'])
    return jsonify({'correct': result})


@app.get('/state')
def state():
    return jsonify(GAME.state())


def create_app():
    return app


if __name__ == '__main__':
    app.run(debug=True)
