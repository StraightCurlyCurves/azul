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

    def make_move(self, factory_id: int, color_id: int, pattern_line_row: int, player_id: int) -> bool:
        assert 0 <= factory_id < len(self._factories)
        assert 0 < color_id <= 4
        assert -1 <= pattern_line_row < 5

        # handle factories
        tiles = self._factories[factory_id].get_and_remove_color_tiles(color_id)
        if tiles.size == 0:
            raise Exception(f'Player {player_id} tried to take a non existing color from a factory.')
        if factory_id > 0:
            self._factories[0].add_tiles(self._factories[factory_id].get_and_remove_tiles())

        # handle playerboard
        temp_out_of_game_tiles = self._playerboards[player_id].place_tiles(tiles, pattern_line_row)
        self._temp_out_of_game_tiles = np.concatenate((self._temp_out_of_game_tiles, temp_out_of_game_tiles))

        return self._is_end_of_round()
    
    def handle_end_of_round(self) -> bool:
        is_end_of_game = False
        for i, pb in enumerate(self._playerboards):
            _is_end_of_game, temp_out_of_game_tiles = pb.handle_end_of_round_and_get_tiles()
            if _is_end_of_game:
                is_end_of_game = True
            if np.count_nonzero(temp_out_of_game_tiles == Symbol.FirstPlayerMarker):
                self._first_player_id = i
            self._temp_out_of_game_tiles = np.concatenate((self._temp_out_of_game_tiles, temp_out_of_game_tiles))
        self._refill_factories()
        self._factories[0].add_tiles(np.array([Symbol.FirstPlayerMarker]))
        return is_end_of_game
    
    def handle_end_of_game(self) -> list:
        player_scores = []
        for pb in self._playerboards:
            final_score = pb.handle_end_of_game()
            player_scores.append(final_score)

        return player_scores
        
    def get_playerboards(self) -> list[Playerboard]:
        return self._playerboards.copy()
    
    def get_factories(self) -> list[Factory]:
        return self._factories.copy()
    
    def _is_end_of_round(self) -> bool:
        n_tiles = 0
        for factory in self._factories:
            n_tiles += factory.get_tiles().size
        return n_tiles == 0
    
    def _refill_factories(self) -> None:
        for factory in self._factories:
            tiles = self._bag_of_tiles.get_and_remove_n_tiles(4)
            if tiles.size < 4:
                self._bag_of_tiles.add_tiles(self._temp_out_of_game_tiles)
            tiles = np.concatenate(tiles, self._bag_of_tiles.get_and_remove_n_tiles(4 - tiles.size))
            factory.add_tiles(tiles)
