import numpy as np

from playerboard import Playerboard
from factory import Factory
from bag import Bag



class Azul:
    '''
    colors:
    0: first player marker
    1: color 1
    2: color 2
    3: color 3
    4: color 4
    '''

    def __init__(self) -> None:
        self._playerboards: list[Playerboard] = []
        self._factories: list[Factory] = [] # factories[0] is the middle pool

        self._bag_of_tiles = Bag()

    def make_move(self, factory_id: int, color_id: int, pattern_line_row: int, player_id: int):
        if not 0 <= factory_id < len(self._factories):
            return -1
        if not 0 < color_id <= 4:
            return -2
        if not 0 <= pattern_line_row <= 5:
            return -3

        # handle factories
        tiles = self._factories[factory_id].get_and_remove_color_tiles(color_id)
        if tiles.size == 0:
            raise Exception(f'Player {player_id} tried to take a non existing color from a factory.')
        if factory_id > 0:
            self._factories[0].add_tiles(self._factories[factory_id].get_and_remove_tiles())

        # handle playerboard
        self._playerboards[player_id].place_tiles(tiles, pattern_line_row)

        # pattern_line = self.playerboards[player_id].get_pattern_lines()[pattern_line_row]
        # if not np.count_nonzero(pattern_line==0) + np.count_nonzero(pattern_line==color_id) == pattern_line_row + 1:
        # self.pools[pool_id].take_color(color_id)
        
    def get_playerboards(self):
        return self._playerboards.copy()
    
    def get_factories(self):
        return self._factories.copy()