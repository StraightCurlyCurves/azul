import numpy as np
from playerboard import Playerboard
from factory import Factory
from bag import Bag

class GameState:

    def __init__(self, players_move_id: int, playerboards: list[Playerboard],
                 factories: list[Factory], bag: Bag, temp_out_of_game_tiles: np.ndarray) -> None:
        self.players_move_id = players_move_id
        self.playerboards = playerboards
        self.factories = factories
        self.bag = bag
        self.temp_out_of_game_tiles = temp_out_of_game_tiles