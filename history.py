from datetime import datetime
import pickle
from copy import deepcopy

from player import Player
from move import Move
from game_state import GameState

# class that stores the whole game state and move for each move
class History:

    def __init__(self) -> None:
        # general game info
        self._players: list[Player] = []
        self._seed = None

        # list of game states and moves: moves[i] is the move that led from game_states[i-1] to game_states[i]
        self._game_states: list[GameState] = []
        self._moves: list[Move] = []
        self._current_game_state_index: int = -1

        # history file ending
        self._history_file_ending = 'azh'

    def move_back(self) -> tuple[GameState, Move]:
        if self._current_game_state_index == -1:
            raise ValueError('No more moves to undo.')
        self._current_game_state_index -= 1
        return self._game_states[self._current_game_state_index], self._moves[self._current_game_state_index]
    
    def move_forward(self) -> tuple[GameState, Move]:
        if self._current_game_state_index == len(self._game_states) - 1:
            raise ValueError('No more moves to redo.')
        self._current_game_state_index += 1
        return self._game_states[self._current_game_state_index], self._moves[self._current_game_state_index]
    
    def update(self, game_state: GameState, move: Move) -> None:
        # delete all game states after the current one
        if self._current_game_state_index < len(self._game_states) - 1:
            self._game_states = self._game_states[:self._current_game_state_index + 1]
        if self._current_game_state_index < len(self._moves) - 1:
            self._moves = self._moves[:self._current_game_state_index + 1]
        self._game_states.append(game_state)
        self._moves.append(move)
        self._current_game_state_index += 1

    def save(self, seed: int = 0, filename: str = None) -> None:
        def getTimeStr(seperator=':'):
            time_format = f"%H{seperator}%M{seperator}%S"
            time = datetime.now()
            return time.strftime(time_format)

        def getDateStr(seperator='-'):
            time_format = f"%Y{seperator}%m{seperator}%d"
            time = datetime.now()
            return time.strftime(time_format)
        if filename is None:
            path = f"{getDateStr('-')}_{getTimeStr('-')}_{len(self._players)}_player_seed_{seed}.{self._history_file_ending}"
        else:
            path = filename
            if not path.endswith(self._history_file_ending):
                path += f'.{self._history_file_ending}'
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    def load(self, path: str) -> None:
        if not path.endswith(self._history_file_ending):
            path += f'.{self._history_file_ending}'
        with open(path, 'rb') as file:
            history: History = pickle.load(file)
            self.__dict__ = history.__dict__
            self._current_game_state_index = 0

    @property
    def players(self) -> list[Player]:
        return deepcopy(self._players)

    @players.setter
    def players(self, players: list[Player]) -> None:
        self._players = players

    @property
    def seed(self):
        return deepcopy(self._seed)
    
    @seed.setter
    def seed(self, seed: int) -> None:
        self._seed = seed

    @property
    def current_game_state(self) -> GameState:
        print(len(self._game_states), self._current_game_state_index)
        return deepcopy(self._game_states[self._current_game_state_index])