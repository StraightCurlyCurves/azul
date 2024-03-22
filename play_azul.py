import numpy as np
from datetime import datetime
from copy import deepcopy

from bot import Bot
from player import Player
from playerboard import Playerboard
from factory import Factory
from bag import Bag
from azul import Azul

class PlayAzul:

    def __init__(self, show_bots_move: bool = True, *args, **kwargs) -> None:
        '''
        Provide either a list of players or a path to a saved game history:

        'players'   - Bot|str: List cointaining a bot or a player name
        'history'   - str: Path to a history file
        '''
        self._show_bots_move = show_bots_move
        
        self._azul: Azul = None
        self._players: list[Player] = []

        # [ [players], [ players_move, [playerboards], [factories], bag, temp_out_of_game_tiles, [move] ] ]
        self._history: list[list[Player], list[tuple[int, list[Playerboard], list[Factory], Bag, np.ndarray, list[int]]]] = [self._players, []]
        self._history_current_index = -1        

        if len(args) > 0:
            raise ValueError('No positional arguments allowed')
        if len(kwargs) != 1:
            raise ValueError(f'{len(kwargs)} arguments given, expected 1.')        
        if not frozenset(kwargs.keys()).issubset(set(('players', 'history'))):
            raise ValueError('Unknown arguments: ' + str(kwargs.keys()))
        if 'players' in kwargs:
            self._seed = np.random.randint(100000)
            np.random.seed(self._seed)
            players = kwargs['players']
            for player in players:
                assert type(player) == str or type(player) == Bot
                self._players.append(Player(player))
            player_count = len(self._players)
            self._azul = Azul(player_count, np.random.randint(player_count))
            self._update_history()
        if 'history' in kwargs:
            self._seed = int(kwargs['history'].split('_')[-1].split('.')[0])
            np.random.seed(self._seed)
            self._history = np.load(kwargs['history'], allow_pickle=True) 
            self._players = self._history[0]
            self._history_current_index = 0
            state = self._history[1][self._history_current_index]
            self._azul = Azul(len(self._players))
            self._azul.set_state(state)

    def play(self):
        is_end_of_game = False
        while not is_end_of_game:
            players_move_id = self._azul.get_players_move_id()
            player = self._players[players_move_id]
            if player.is_bot:
                move = player.bot.get_move(self._azul.get_factories(),
                                           self._azul.get_playerboards())
                if self._show_bots_move:
                    self._azul.print_state(self._players)
                    print(f"Bot's move:", move)
                    input('Press enter to continue...')
                try:
                    is_end_of_game = self._azul.make_move(*move, player_id=players_move_id)
                    self._update_history([*move, players_move_id])
                except Exception as e:
                    print(repr(e))
                    self._save_history(self._seed)
                    print(f"Bot '{player.name}' messed up. History saved.")
                    exit()
            else:
                self._azul.print_state(self._players)
                factory_id = input(f'Factory ID: ')
                if factory_id == 'b':
                    self._history_move_back()
                    continue
                elif factory_id == 'f':
                    self._history_move_forward()
                    continue
                elif factory_id == 'q':
                    self._save_history(self._seed)
                    print('Saved game and quit.')
                    break
                else:
                    try:
                        factory_id = int(factory_id)
                    except:
                        input('Not a valid input. Press Enter to try again.')
                        continue

                color_id = input(f'Color ID: ')
                if color_id == 'c': continue  
                else:
                    try:
                        color_id = int(color_id)
                    except:
                        input('Not a valid input. Press Enter to try again.')
                        continue

                pattern_line_row = input(f'Pattern line row: ')
                if pattern_line_row == 'c': continue
                else:
                    try:
                        pattern_line_row = int(pattern_line_row)
                    except:
                        input('Not a valid input. Press Enter to try again.')
                        continue

                try:
                    is_end_of_game = self._azul.make_move(factory_id, color_id, pattern_line_row, players_move_id)
                    self._update_history([factory_id, color_id, pattern_line_row, players_move_id])
                except Exception as e:
                    print(repr(e))
                    input('Press Enter to try again.')
                    continue
                
            if is_end_of_game:
                self._azul.print_state(self._players)
                console_input = input("End of game. Press Enter to save and quit or 'b' to go back one move.")
                if console_input == 'b':
                    self._history_move_back()
                    is_end_of_game = False
                else:
                    self._save_history(self._seed)

    def _update_history(self, move: list[int] = []) -> None:
        if self._history_current_index < len(self._history[1])-1:
            self._history[1] = self._history[1][:self._history_current_index+1]
        state = (*self._azul.get_state(), deepcopy(move))
        self._history[1].append(state)
        self._history_current_index += 1

    def _save_history(self, seed=0):
        def getTimeStr(seperator=':'):
            time_format = f"%H{seperator}%M{seperator}%S"
            time = datetime.now()
            return time.strftime(time_format)

        def getDateStr(seperator='-'):
            time_format = f"%Y{seperator}%m{seperator}%d"
            time = datetime.now()
            return time.strftime(time_format)
        path = f"history_{getDateStr('-')}_{getTimeStr('-')}_{self._azul.get_player_count()}_player_seed_{seed}.npy"
        np.save(path, np.array(self._history, dtype=object), allow_pickle=True)

    def _history_move_back(self) -> bool:
        if self._history_current_index > 0:
            self._history_current_index -= 1
            state = self._history[1][self._history_current_index]
            self._azul.set_state(state)
            return True
        else:
            return False
    
    def _history_move_forward(self) -> bool:
        if self._history_current_index < len(self._history[1])-1:
            self._history_current_index += 1
            state = self._history[1][self._history_current_index]
            self._azul.set_state(state)
            print('True')
            return True
        else:
            print('False')
            return False
        
if __name__ == '__main__':
    game = PlayAzul(players=['P1', 'P2'])
    # game = PlayAzul(history='history_???.npy')
    game.play()