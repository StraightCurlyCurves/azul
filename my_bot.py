import numpy as np
from bot import Bot
from factory import Factory
from playerboard import Playerboard
from symbols import Symbol
from move import Move

class MyBot(Bot):

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def get_move(self, factories: list[Factory], playerboards: list[Playerboard], player_id: int) -> Move:
        factory_id = None
        color_id = None
        pattern_line_row = None

        # find a valid factory to take tiles from
        for i, factory in enumerate(factories):
            factory_id = i
            tiles = factory.tiles
            valid_tiles_mask = tiles != Symbol.FirstPlayerMarker
            if valid_tiles_mask.any():
                color_id = tiles[valid_tiles_mask][0]
                break
        
        # optional: try to find a valid pattern line to place at least one tile
        playerboard = playerboards[player_id]
        for i, pattern_line in enumerate(playerboard.pattern_lines):
            wall_line = playerboard.wall[i]
            color_not_in_wall_line = color_id not in wall_line
            pattern_line_has_different_color = np.count_nonzero(pattern_line != Symbol.EmptyField) \
                  != np.count_nonzero(pattern_line == color_id)
            pattern_line_is_not_full = np.count_nonzero(pattern_line == Symbol.EmptyField) > 0
            if color_not_in_wall_line and not pattern_line_has_different_color and pattern_line_is_not_full:
                pattern_line_row = i
                break
            else:
                pattern_line_row = -1
            
        return Move(factory_id, color_id, pattern_line_row)