import numpy as np

from playerboard import Playerboard
from factory import Factory
from bag import Bag
from symbols import Symbol



class Azul:

    def __init__(self, first_player_id=0) -> None:
        self._first_player_id = first_player_id
        self._playerboards: list[Playerboard] = []
        self._factories: list[Factory] = [] # factories[0] is the middle pool

        self._bag_of_tiles = Bag()
        self._temp_out_of_game_tiles = np.array([], dtype=int)

    def make_move(self, factory_id: int, color_id: int, pattern_line_row: int, player_id: int):
        if not 0 <= factory_id < len(self._factories):
            return -1
        if not 0 < color_id <= 4:
            return -2
        if not -1 <= pattern_line_row < 5:
            return -3

        # handle factories
        tiles = self._factories[factory_id].get_and_remove_color_tiles(color_id)
        if tiles.size == 0:
            raise Exception(f'Player {player_id} tried to take a non existing color from a factory.')
        if factory_id > 0:
            self._factories[0].add_tiles(self._factories[factory_id].get_and_remove_tiles())

        # handle playerboard
        temp_out_of_game_tiles = self._playerboards[player_id].place_tiles(tiles, pattern_line_row)
        self._temp_out_of_game_tiles = np.concatenate((self._temp_out_of_game_tiles, temp_out_of_game_tiles))

        return self._is_end_of_turn()
    
    def handle_end_of_turn(self):
        for i, pb in enumerate(self._playerboards):
            temp_out_of_game_tiles = pb.handle_end_of_turn_and_get_tiles() # TODO
            if np.count_nonzero(temp_out_of_game_tiles == Symbol.FirstPlayerMarker):
                self._first_player_id = i
            self._temp_out_of_game_tiles = np.concatenate((self._temp_out_of_game_tiles, temp_out_of_game_tiles))
        self._refill_factories() # TODO
        
    def get_playerboards(self):
        return self._playerboards.copy()
    
    def get_factories(self):
        return self._factories.copy()
    
    def _is_end_of_turn(self):
        n_tiles = 0
        for factory in self._factories:
            n_tiles += factory.get_tiles().size
        return n_tiles == 0