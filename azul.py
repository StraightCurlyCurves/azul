import os
import numpy as np
from datetime import datetime

from playerboard import Playerboard
from factory import Factory
from bag import Bag
from symbols import Symbol
from cmd_colors import Colors
from player import Player

from copy import deepcopy

class Azul:

    def __init__(self, player_count=2, first_player_id=0) -> None:
        self._player_count = player_count
        self._players_move_id = first_player_id
        self._playerboards: list[Playerboard] = []
        self._factories: list[Factory] = [] # factories[0] is the middle pool

        self._bag_of_tiles = Bag()
        self._temp_out_of_game_tiles = np.array([], dtype=int)

        self._setup_game()        

    def make_move(self, factory_id: int, color_id: int, pattern_line_row: int, player_id: int) -> bool:
        assert 0 <= factory_id < len(self._factories), 'Invalid factory ID'
        assert Symbol.is_valid_color(color_id), 'Invalid color ID'
        assert -1 <= pattern_line_row < 5, 'Invalid pattern line row'
        assert 0 <= player_id < len(self._playerboards), 'Invalid player ID'

        # handle factories
        tiles = self._factories[factory_id].get_and_remove_color_tiles(color_id)
        if tiles.size == 0:
            raise Exception(f'Player {player_id} tried to take a non existing color from a factory.')
        if factory_id > 0:
            self._factories[0].add_tiles(self._factories[factory_id].get_and_remove_tiles())

        # handle playerboard
        temp_out_of_game_tiles = self._playerboards[player_id].place_tiles(tiles, pattern_line_row)
        self._temp_out_of_game_tiles = np.concatenate((self._temp_out_of_game_tiles, temp_out_of_game_tiles))

        # players move
        self._players_move_id += 1
        self._players_move_id %= self._player_count

        # check game state, return is_end_of_game
        is_end_of_game = False
        if self._is_end_of_round():
            is_end_of_game = self._handle_end_of_round()
            if is_end_of_game:
                self._players_move_id = -1
                for pb in self._playerboards:
                    _ = pb.handle_end_of_game()
        self.check_integrity()   
        return is_end_of_game    
    
    def get_state(self) -> tuple[int, list[Playerboard], list[Factory], Bag, np.ndarray, list[int]]:
        state = (deepcopy(self._players_move_id),
                 deepcopy(self._playerboards),
                 deepcopy(self._factories),
                 deepcopy(self._bag_of_tiles),
                 deepcopy(self._temp_out_of_game_tiles))
        return state
    
    def set_state(self, state):
        self._players_move_id = deepcopy(state[0])
        self._playerboards = deepcopy(state[1])
        self._factories = deepcopy(state[2])
        self._bag_of_tiles = deepcopy(state[3])
        self._temp_out_of_game_tiles = deepcopy(state[4])

    def check_integrity(self) -> None:
        all_tiles = np.array([], dtype=int)
        all_tiles = np.concatenate((all_tiles, self._temp_out_of_game_tiles))
        all_tiles = np.concatenate((all_tiles, self._bag_of_tiles._tiles))
        for f in self._factories:
            all_tiles = np.concatenate((all_tiles, f._tiles))
        for pb in self._playerboards:
            all_tiles = np.concatenate((all_tiles, pb._floor_line[pb._floor_line!=Symbol.EmptyField]))
            for pl in pb._pattern_lines:
                all_tiles = np.concatenate((all_tiles, pl[pl!=Symbol.EmptyField]))
            for wl in pb._wall:
                all_tiles = np.concatenate((all_tiles, wl[wl!=Symbol.EmptyField]))
        assert all_tiles[all_tiles==Symbol.Color1].size == 20, 'Integrity check failed.'
        assert all_tiles[all_tiles==Symbol.Color2].size == 20, 'Integrity check failed.'
        assert all_tiles[all_tiles==Symbol.Color3].size == 20, 'Integrity check failed.'
        assert all_tiles[all_tiles==Symbol.Color4].size == 20, 'Integrity check failed.'
        assert all_tiles[all_tiles==Symbol.Color5].size == 20, 'Integrity check failed.'

    def get_playerboards(self) -> list[Playerboard]:
        return deepcopy(self._playerboards)
    
    def get_factories(self) -> list[Factory]:
        return deepcopy(self._factories)
    
    def get_players_move_id(self):
        return self._players_move_id
    
    def get_player_count(self) -> int:
        return self._player_count
    
    def print_state(self, players: list[Player] = None) -> None:
        def mv_c(row, col):
            print(f'\033[{row};{col}H', end='')
        bag_width = 15
        bag_row_count = 1
        bag_row_start = 1
        temp_out_of_game_tiles_count = 1
        c_row, c_col = 0, 0
        spaces = ''
        for i in range(os.get_terminal_size().lines):
            spaces += '\n'
        print(spaces)
        mv_c(0,0)

        print('Bag:')
        esc_string = ''
        for i, tile in enumerate(self._bag_of_tiles._tiles):
            if i > 0 and i%bag_width == 0:
                esc_string += '\n'
                bag_row_count += 1
            if tile == Symbol.Color1: esc_string += f'{Colors.c1}{Symbol.Color1}{Colors.reset} '
            if tile == Symbol.Color2: esc_string += f'{Colors.c2}{Symbol.Color2}{Colors.reset} '
            if tile == Symbol.Color3: esc_string += f'{Colors.c3}{Symbol.Color3}{Colors.reset} '
            if tile == Symbol.Color4: esc_string += f'{Colors.c4}{Symbol.Color4}{Colors.reset} '
            if tile == Symbol.Color5: esc_string += f'{Colors.c5}{Symbol.Color5}{Colors.reset} '
            if tile == Symbol.FirstPlayerMarker: esc_string += f'{Colors.fpm}{Symbol.FirstPlayerMarker}{Colors.reset} '
            if tile == Symbol.EmptyField: esc_string += f'{Colors.ef}{Symbol.EmptyField}{Colors.reset} '
        print(esc_string, end='')

        c_row, c_col = bag_row_start, 2*bag_width+3
        mv_c(c_row, c_col)
        print('Factories:', end='')
        for i, f in enumerate(self._factories):
            c_row += 1
            mv_c(c_row, c_col)
            print(f'{i}: ', end='')
            for tile in f._tiles:
                if tile == Symbol.Color1: print(f'{Colors.c1}{Symbol.Color1}{Colors.reset} ', end='')
                if tile == Symbol.Color2: print(f'{Colors.c2}{Symbol.Color2}{Colors.reset} ', end='')
                if tile == Symbol.Color3: print(f'{Colors.c3}{Symbol.Color3}{Colors.reset} ', end='')
                if tile == Symbol.Color4: print(f'{Colors.c4}{Symbol.Color4}{Colors.reset} ', end='')
                if tile == Symbol.Color5: print(f'{Colors.c5}{Symbol.Color5}{Colors.reset} ', end='')
                if tile == Symbol.FirstPlayerMarker: print(f'{Colors.fpm}{Symbol.FirstPlayerMarker}{Colors.reset} ', end='')
                if tile == Symbol.EmptyField: print(f'{Colors.ef}{Symbol.EmptyField}{Colors.reset} ', end='')

        if bag_row_count >= len(self._factories):
            c_row, c_col = bag_row_start+bag_row_count+2, 0
            mv_c(c_row, c_col)  
        else:
            c_row, c_col = bag_row_start+len(self._factories)+2, 0
            mv_c(c_row, c_col)

        print('Temp out of game tiles:', end='')
        c_row += 1
        mv_c(c_row, c_col)
        if self._temp_out_of_game_tiles.size == 0:
            temp_out_of_game_tiles_count += 1
            print(f'{Colors.ef}[]{Colors.reset} ', end='')
        for i, tile in enumerate(self._temp_out_of_game_tiles):
            if i > 0 and i%bag_width == 0:
                c_row += 1
                mv_c(c_row, c_col)
                temp_out_of_game_tiles_count += 1
            if tile == Symbol.Color1: print(f'{Colors.c1}{Symbol.Color1}{Colors.reset} ', end='')
            if tile == Symbol.Color2: print(f'{Colors.c2}{Symbol.Color2}{Colors.reset} ', end='')
            if tile == Symbol.Color3: print(f'{Colors.c3}{Symbol.Color3}{Colors.reset} ', end='')
            if tile == Symbol.Color4: print(f'{Colors.c4}{Symbol.Color4}{Colors.reset} ', end='')
            if tile == Symbol.Color5: print(f'{Colors.c5}{Symbol.Color5}{Colors.reset} ', end='')
            if tile == Symbol.FirstPlayerMarker: print(f'{Colors.fpm}{Symbol.FirstPlayerMarker}{Colors.reset} ', end='')
            if tile == Symbol.EmptyField: print(f'{Colors.ef}{Symbol.EmptyField}{Colors.reset} ', end='')
        c_row += 3
        mv_c(c_row, c_col)

        player_width = 33
        for player_id, pb in enumerate(self._playerboards):
            player_row = c_row
            c_col = player_id*player_width

            if player_id == self._players_move_id:
                color_format = Colors.bg_green + Colors.italic + Colors.black
            else:
                color_format = Colors.underline + Colors.italic
            if type(players) != None:
                print(f'{color_format}{players[player_id].name}:{Colors.reset}')
            else:
                print(f'{color_format}Player {player_id}:{Colors.reset}')
            c_row += 1
            mv_c(c_row, c_col)
            print('Pattern lines:', end='')
            pl_width = 14
            for i, pl in enumerate(pb._pattern_lines):
                c_row += 1
                c_col = player_id*player_width + pl_width-2*i
                mv_c(c_row, c_col)
                for tile in pl:
                    if tile == Symbol.Color1: print(f'{Colors.c1}{Symbol.Color1}{Colors.reset} ', end='')
                    if tile == Symbol.Color2: print(f'{Colors.c2}{Symbol.Color2}{Colors.reset} ', end='')
                    if tile == Symbol.Color3: print(f'{Colors.c3}{Symbol.Color3}{Colors.reset} ', end='')
                    if tile == Symbol.Color4: print(f'{Colors.c4}{Symbol.Color4}{Colors.reset} ', end='')
                    if tile == Symbol.Color5: print(f'{Colors.c5}{Symbol.Color5}{Colors.reset} ', end='')
                    if tile == Symbol.FirstPlayerMarker: print(f'{Colors.fpm}{Symbol.FirstPlayerMarker}{Colors.reset} ', end='')
                    if tile == Symbol.EmptyField: print(f'{Colors.ef}_{Colors.reset} ', end='')
                
                c_col = player_id*player_width
                mv_c(c_row, c_col)
                print(f'{i}: ')

            c_row = player_row + 1
            c_col = player_id*player_width + pl_width + 4
            mv_c(c_row, c_col)
            print('Wall:', end='')
            for i, wl in enumerate(pb._wall):
                c_row += 1
                mv_c(c_row, c_col)
                for j, tile in enumerate(wl):
                    color_id = pb._wall_colors[i, j]
                    if color_id == Symbol.Color1: color = Colors.c1
                    if color_id == Symbol.Color2: color = Colors.c2
                    if color_id == Symbol.Color3: color = Colors.c3
                    if color_id == Symbol.Color4: color = Colors.c4
                    if color_id == Symbol.Color5: color = Colors.c5
                    if color_id == Symbol.EmptyField: color = Colors.ef
                    if tile == Symbol.Color1: print(f'{color}X{Colors.reset} ', end='')
                    if tile == Symbol.Color2: print(f'{color}X{Colors.reset} ', end='')
                    if tile == Symbol.Color3: print(f'{color}X{Colors.reset} ', end='')
                    if tile == Symbol.Color4: print(f'{color}X{Colors.reset} ', end='')
                    if tile == Symbol.Color5: print(f'{color}X{Colors.reset} ', end='')
                    if tile == Symbol.FirstPlayerMarker: print(f'{color}X{Colors.reset} ', end='')
                    if tile == Symbol.EmptyField: print(f'{color}_{Colors.reset} ', end='')

            c_row += 2
            c_col = player_id*player_width
            mv_c(c_row, c_col)
            print('Floor line:', end='')
            c_col = player_id*player_width + pl_width + 4
            mv_c(c_row, c_col)
            print(f'Score: {pb._score}')
            c_row += 1
            c_col = player_id*player_width
            mv_c(c_row, c_col)
            for tile in pb._floor_line:
                if tile == Symbol.Color1: print(f'{Colors.c1}{Symbol.Color1}{Colors.reset} ', end='')
                if tile == Symbol.Color2: print(f'{Colors.c2}{Symbol.Color2}{Colors.reset} ', end='')
                if tile == Symbol.Color3: print(f'{Colors.c3}{Symbol.Color3}{Colors.reset} ', end='')
                if tile == Symbol.Color4: print(f'{Colors.c4}{Symbol.Color4}{Colors.reset} ', end='')
                if tile == Symbol.Color5: print(f'{Colors.c5}{Symbol.Color5}{Colors.reset} ', end='')
                if tile == Symbol.FirstPlayerMarker: print(f'{Colors.fpm}{Symbol.FirstPlayerMarker}{Colors.reset} ', end='')
                if tile == Symbol.EmptyField: print(f'{Colors.ef}_{Colors.reset} ', end='')
            c_row += 1
            c_col = player_id*player_width
            mv_c(c_row, c_col)
            print(f'{Colors.ef}1 1 2 2 2 3 3{Colors.reset}', end='')
            if player_id < len(self._playerboards)-1:
                c_row = player_row
                c_col = (player_id+1)*player_width
                mv_c(c_row, c_col)

        c_row += 3
        c_col = 0
        mv_c(c_row, c_col)
    
    def _setup_game(self):
        n_players = self._player_count
        assert 2 <= n_players <= 4
        for _ in range(n_players):
            self._playerboards.append(Playerboard())
        if n_players == 2:
            for i in range(5+1):
                self._factories.append(Factory())
        if n_players == 3:
            for i in range(7+1):
                self._factories.append(Factory())
        if n_players == 4:
            for i in range(9+1):
                self._factories.append(Factory())
        self._factories[0].add_tiles(np.array([Symbol.FirstPlayerMarker]))
        self._refill_factories()        
    
    def _is_end_of_round(self) -> bool:
        n_tiles = 0
        for factory in self._factories:
            n_tiles += factory.get_tiles().size
        return n_tiles == 0    
        
    def _handle_end_of_round(self) -> bool:
        is_end_of_game = False
        for i, pb in enumerate(self._playerboards):
            _is_end_of_game, temp_out_of_game_tiles = pb.handle_end_of_round_and_get_tiles()
            if _is_end_of_game:
                is_end_of_game = True
            if np.count_nonzero(temp_out_of_game_tiles == Symbol.FirstPlayerMarker):
                self._players_move_id = i
            self._temp_out_of_game_tiles = np.concatenate((self._temp_out_of_game_tiles, temp_out_of_game_tiles))
        self._refill_factories()
        return is_end_of_game
    
    def _refill_factories(self) -> None:
        mask_fpm = self._temp_out_of_game_tiles == Symbol.FirstPlayerMarker
        self._factories[0].add_tiles(self._temp_out_of_game_tiles[mask_fpm])
        self._temp_out_of_game_tiles = self._temp_out_of_game_tiles[~mask_fpm]
        for factory in self._factories[1:]:
            tiles = self._bag_of_tiles.get_and_remove_n_tiles(4)
            if tiles.size < 4:
                self._bag_of_tiles.add_tiles(self._temp_out_of_game_tiles)
            tiles = np.concatenate((tiles, self._bag_of_tiles.get_and_remove_n_tiles(4 - tiles.size)))
            factory.add_tiles(tiles)
