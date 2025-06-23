from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class Player:
    name: str
    word: Optional[str] = None
    company: Optional[str] = None  # CEO name if acquired

    def is_free(self) -> bool:
        return self.company is None

    def __repr__(self) -> str:  # helpful for debugging
        return f"Player(name={self.name}, word={self.word}, company={self.company})"


@dataclass
class Game:
    players: Dict[str, Player] = field(default_factory=dict)
    words: Dict[str, str] = field(default_factory=dict)  # word -> player name
    ceo: Optional[str] = None
    employees: Dict[str, Set[str]] = field(default_factory=dict)  # CEO -> employees
    started: bool = False

    def add_player(self, name: str) -> None:
        if name in self.players:
            raise ValueError("Player already exists")
        self.players[name] = Player(name)

    def submit_word(self, name: str, word: str) -> None:
        if name not in self.players:
            raise ValueError("Player not found")
        if self.started:
            raise ValueError("Game already started")
        if word in self.words:
            raise ValueError("Word already used")
        self.players[name].word = word
        self.words[word] = name

    def start(self) -> List[str]:
        if self.started:
            raise ValueError("Game already started")
        missing = [p.name for p in self.players.values() if not p.word]
        if missing:
            raise ValueError(f"Players missing words: {missing}")
        self.started = True
        return list(self.words.keys())

    def guess(self, guesser: str, target: str, word_guess: str) -> bool:
        if not self.started:
            raise ValueError("Game not started")
        if guesser not in self.players or target not in self.players:
            raise ValueError("Invalid players")
        if word_guess not in self.words:
            raise ValueError("Unknown word")
        real_owner = self.words[word_guess]
        if real_owner == target:
            # correct guess
            self._acquire(guesser, target)
            return True
        else:
            # wrong guess -> new CEO
            self.ceo = target
            return False

    def _acquire(self, ceo: str, employee: str) -> None:
        self.ceo = ceo
        self.players[employee].company = ceo
        if ceo not in self.employees:
            self.employees[ceo] = set()
        self.employees[ceo].add(employee)

    def state(self) -> Dict[str, any]:
        return {
            "players": {name: vars(p) for name, p in self.players.items()},
            "ceo": self.ceo,
            "employees": {ceo: list(e) for ceo, e in self.employees.items()},
            "started": self.started,
        }
