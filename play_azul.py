import sys
if sys.version_info < (3, 10):
    sys.exit("Script requires Python 3.10 or higher")

import numpy as np
from copy import deepcopy

from bot import Bot
from player import Player
from azul import Azul
from history import History
from move import Move

from my_bot import MyBot

VERSION = '1.0.0'

class PlayAzul:

    def __init__(self, players: list[Bot|str] = None, history: str = None,
                 show_bots_move: bool = True, save_history: bool = True, history_file_name: str = None) -> None:
        '''
        Provide either a list of players or a path to a saved game history or both to overwrite the players saved in the history:

        'players'   - Bot|str: List cointaining a bot or a player name
        'history'   - str: Path to a history file
        '''
        # save input parameters for game reset
        self.__players = deepcopy(players)
        self.__history = deepcopy(history)
        self.__show_bots_move = show_bots_move
        self.__save_history = save_history

        self._show_bots_move = show_bots_move
        self._save_history = save_history
        self._history_file_name = history_file_name
        
        self._azul: Azul = None
        self._players: list[Player] = []

        self._history = History()

        if players is None and history is None:
            raise ValueError('Provide either a list of players or a path to a saved game history.')
            
        if players is not None and history is None:
            self._seed = np.random.randint(100000)
            np.random.seed(self._seed)
            self._history.seed = self._seed
            if len(players) < 2:
                raise ValueError('At least 2 players required.')
            if len(players) > 4:
                raise ValueError('At most 4 players allowed.')
            for i, player in enumerate(players):
                if not isinstance(player, (str, Bot)):
                    raise TypeError(f'Player must be of type str or Bot, not {type(player).__name__}')
                self._players.append(Player(player, player_id=i))
            player_count = len(self._players)
            self._azul = Azul(player_count, np.random.randint(player_count))
            self._history.players = self._players
            self._history.update(self._azul.get_game_state(), [])

        if history is not None:
            self._history.load(history)            
            self._seed = self._history.seed
            np.random.seed(self._seed)
            if players is None:          
                self._players = self._history.players
            else:
                if len(players) != len(self._history.players):
                    raise ValueError('Number of players in history does not match number of players provided.')
                for i, player in enumerate(players):
                    if not isinstance(player, (str, Bot)):
                        raise TypeError(f'Player must be of type str or Bot, not {type(player).__name__}')
                    self._players.append(Player(player, player_id=i))
                self._history.players = self._players
            state = self._history.current_game_state
            self._azul = Azul(len(self._players))
            self._azul.set_game_state(state)

    def play(self) -> list[tuple[str, int, int]]:
        is_end_of_game = False
        while not is_end_of_game:
            players_move_id = self._azul.players_move_id
            player = self._players[players_move_id]
            if player.is_bot:
                move = player._bot.get_move(self._azul.factories,
                                           self._azul.playerboards,
                                           player.player_id)
                if self._show_bots_move:
                    self._azul.print_state(self._players)
                    print(f"Bot's move:", move)
                    input('Press enter to continue...')
                try:
                    is_end_of_game = self._azul.make_move(*move)
                    self._history.update(self._azul.get_game_state(), move)
                except Exception as e:
                    print(repr(e))
                    if self._save_history: self._history.save(self._seed, self._history_file_name)
                    print(f"Bot '{player.name}' messed up. History saved.")
                    break
            else:
                self._azul.print_state(self._players)
                factory_id = input(f'Factory ID: ')
                if factory_id == 'b':
                    self._move_back()
                    continue
                elif factory_id == 'f':
                    self._move_forward()
                    continue
                elif factory_id == 'q':
                    if self._save_history: self._history.save(self._seed, self._history_file_name)
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
                
                move = Move(factory_id, color_id, pattern_line_row)
                try:
                    is_end_of_game = self._azul.make_move(factory_id, color_id, pattern_line_row)
                    self._history.update(self._azul.get_game_state(), move)
                except Exception as e:
                    print(repr(e))
                    input('Press Enter to try again.')
                    continue
                
            if is_end_of_game:
                if self._show_bots_move:
                    self._azul.print_state(self._players)
                    console_input = input("End of game. Press Enter to save and quit or 'b' to go back one move.")
                    if console_input == 'b':
                        self._move_back()
                        is_end_of_game = False
                else:
                    if self._save_history:
                        self._history.save(self._seed, self._history_file_name)
                        print('Saved game and quit.')

        # create list with player name, player id and score, sorted by score
        players_score = self._azul.get_players_score()
        ranklist = sorted([(player.name, player.player_id, score) for player, score in \
            zip(self._players, players_score)], key=lambda x: x[2], reverse=True)

        self.__dict__ = PlayAzul(self.__players, self.__history, self.__show_bots_move, self.__save_history).__dict__
        return ranklist
    
    def _move_forward(self) -> bool:
        try:
            game_state, _ = self._history.move_forward()
            self._azul.set_game_state(game_state)
        except Exception as e:
            print(repr(e))
    
    def _move_back(self) -> bool:
        try:
            game_state, _ = self._history.move_back()
            self._azul.set_game_state(game_state)
        except Exception as e:
            print(repr(e))

        
if __name__ == '__main__':
    ### Play a game with two friends ###
    players = ['Me', 'Myself', 'I']
    game = PlayAzul(players=players)
    ranklist = game.play()
    for i, rank in enumerate(ranklist):
        print(f'{i+1}. {rank[0]}, Score: {rank[2]}')

    ### Play a game against a bot ###
    bot = MyBot('Bot')
    players = ['Me', bot]
    game = PlayAzul(players=players)
    ranklist = game.play()
    for i, rank in enumerate(ranklist):
        print(f'{i+1}. {rank[0]}, Score: {rank[2]}')

    ### Let three bots play against each other ###
    bot_1 = MyBot('Bot 1')
    bot_2 = MyBot('Bot 2')
    bot_3 = MyBot('Bot 3')
    players=[bot_1, bot_2, bot_3]
    game = PlayAzul(players=players, history_file_name='bot_game', show_bots_move=False)
    ranklist = game.play()
    for i, rank in enumerate(ranklist):
        print(f'{i+1}. {rank[0]}, Score: {rank[2]}')

    ### Load a game played by bots but play and alternate it manually ###
    players = ['Me', 'Myself', 'I']
    game = PlayAzul(players=players, history='bot_game')
    ranklist = game.play()
    for i, rank in enumerate(ranklist):
        print(f'{i+1}. {rank[0]}, Score: {rank[2]}')

    ### Simulate 1000 games between two bots ###
    bot_1 = MyBot('Bot 1')
    bot_2 = MyBot('Bot 2')
    players=[bot_1, bot_2]
    game = PlayAzul(players=players, show_bots_move=False, save_history=False)
    wins = [0]*len(players)
    for i in range(1000):
        ranklist = game.play()
        winner_id = ranklist[0][1]
        wins[winner_id] += 1
        print('\r', end='')
        print(f'{i+1} games played', end='')
    print('Wins:', wins)