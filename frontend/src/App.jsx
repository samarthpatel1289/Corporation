import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [playerName, setPlayerName] = useState('');
  const [word, setWord] = useState('');
  const [guesser, setGuesser] = useState('');
  const [target, setTarget] = useState('');
  const [guessWord, setGuessWord] = useState('');
  const [state, setState] = useState({});

  const refresh = async () => {
    const res = await fetch('/state');
    const data = await res.json();
    setState(data);
  };

  useEffect(() => { refresh(); }, []);

  const addPlayer = async () => {
    if (!playerName) return;
    await fetch('/players', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: playerName })
    });
    setPlayerName('');
    refresh();
  };

  const submitWord = async () => {
    if (!playerName || !word) return;
    await fetch('/submit-word', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: playerName, word })
    });
    setWord('');
    refresh();
  };

  const startGame = async () => {
    await fetch('/start', { method: 'POST' });
    refresh();
  };

  const guess = async () => {
    if (!guesser || !target || !guessWord) return;
    await fetch('/guess', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ guesser, target, word: guessWord })
    });
    setGuessWord('');
    refresh();
  };

  return (
    <div className="container py-3">
      <h1 className="mb-4">The Corporation</h1>

      <div className="mb-3">
        <input className="form-control" placeholder="Player name" value={playerName} onChange={e => setPlayerName(e.target.value)} />
        <button className="btn btn-primary mt-2" onClick={addPlayer}>Add Player</button>
      </div>

      <div className="mb-3">
        <input className="form-control" placeholder="Word" value={word} onChange={e => setWord(e.target.value)} />
        <button className="btn btn-primary mt-2" onClick={submitWord}>Submit Word</button>
      </div>

      <button className="btn btn-success mb-3" onClick={startGame}>Start Game</button>

      <div className="mb-3">
        <input className="form-control" placeholder="Guesser" value={guesser} onChange={e => setGuesser(e.target.value)} />
        <input className="form-control mt-2" placeholder="Target" value={target} onChange={e => setTarget(e.target.value)} />
        <input className="form-control mt-2" placeholder="Word Guess" value={guessWord} onChange={e => setGuessWord(e.target.value)} />
        <button className="btn btn-warning mt-2" onClick={guess}>Guess</button>
      </div>

      <pre>{JSON.stringify(state, null, 2)}</pre>
    </div>
  );
}

export default App;
