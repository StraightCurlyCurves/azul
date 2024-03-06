import numpy as np
from symbols import Symbol

class Playerboard:
    
    def __init__(self) -> None:
        self._score = 0
        self._wall = np.zeros((5,5), dtype=int)
        self._pattern_lines: list[np.ndarray] = []
        for i in range(6):
            self._pattern_lines.append(np.zeros(i, dtype=int))
        self._floor_line = np.zeros(7, dtype=int)

        self._floor_line_val = np.array([-1, -1, -2, -2, -2, -3, -3], dtype=int)
        self._wall_colors = np.array([[1,2,3,4,5],
                                      [5,1,2,3,4],
                                      [4,5,1,2,3],
                                      [3,4,5,1,2],
                                      [2,3,4,5,1]])

    def place_tiles(self, tiles: np.ndarray, pattern_line_row: int) -> np.ndarray:
        '''
        Places tiles on a specific pattern line. Tiles that cannot be placed there will automatically be placed on the floor line.
        pattern_line_row: -1 places all tiles to the floor.
        Returns tiles which didn't fit on the floor line anymore (but never the first player marker).
        '''
        temp_out_of_game_tiles = np.array([], dtype=int)

        if pattern_line_row < 0:
            temp_out_of_game_tiles = np.concatenate((temp_out_of_game_tiles,
                                                     self._place_tiles_on_floor_line(tiles)))
            return temp_out_of_game_tiles
        
        color_id = tiles[0]
        wall_line_has_color = np.count_nonzero(self._wall[pattern_line_row] == color_id)
        pattern_line_is_full = np.count_nonzero(self._pattern_lines[pattern_line_row]) == \
            self._pattern_lines[pattern_line_row].size
        pattern_line_has_different_color = np.count_nonzero(self._pattern_lines[pattern_line_row]) != \
            np.count_nonzero(self._pattern_lines[pattern_line_row] == color_id)
        if wall_line_has_color or pattern_line_is_full or pattern_line_has_different_color:
            temp_out_of_game_tiles = np.concatenate((temp_out_of_game_tiles,
                                                     self._place_tiles_on_floor_line(tiles)))
        else:
            temp_out_of_game_tiles = np.concatenate((temp_out_of_game_tiles,
                                                     self._place_tiles_on_pattern_line(tiles, pattern_line_row)))

        return temp_out_of_game_tiles

    def _place_tiles_on_floor_line(self, tiles: np.ndarray) -> np.ndarray:
        temp_out_of_game_tiles = np.array([], dtype=int)

        # place first player marker if available and exchange it in case floor line is full
        mask_first_player_marker = tiles==Symbol.FirstPlayerMarker
        if np.count_nonzero(mask_first_player_marker):
            mask_empty_fields = self._floor_line == 0
            empty_fields: np.ndarray = self._floor_line[mask_empty_fields]
            if empty_fields.size > 0:
                empty_fields[0] = Symbol.FirstPlayerMarker
            else:
                temp_out_of_game_tiles = np.concatenate((temp_out_of_game_tiles,
                                                         self._floor_line[:1]))
                self._floor_line[0] = Symbol.FirstPlayerMarker
            tiles = tiles[~mask_first_player_marker]
            self._floor_line[mask_empty_fields] = empty_fields

        # place as many tiles as possible to the floor line
        mask_empty_fields = self._floor_line == 0
        empty_fields: np.ndarray = self._floor_line[mask_empty_fields]
        if empty_fields.size < tiles.size:
            empty_fields = tiles[:empty_fields.size]
            temp_out_of_game_tiles = np.concatenate((temp_out_of_game_tiles,
                                                     tiles[empty_fields.size:]))
        else:
            empty_fields[:tiles.size] = tiles
        self._floor_line[mask_empty_fields] = empty_fields

        return temp_out_of_game_tiles
    
    def _place_tiles_on_pattern_line(self, tiles: np.ndarray, pattern_line_row: int) -> np.ndarray:
        temp_out_of_game_tiles = np.array([], dtype=int)

        mask_empty_fields = self._pattern_lines[pattern_line_row] == 0
        empty_fields: np.ndarray = self._pattern_lines[pattern_line_row][mask_empty_fields]
        if empty_fields.size < tiles.size:
            empty_fields = tiles[:empty_fields.size]
            temp_out_of_game_tiles = np.concatenate((temp_out_of_game_tiles,
                                                     self._place_tiles_on_floor_line(tiles[empty_fields.size:])))
        else:
            empty_fields[empty_fields.size-tiles.size:] = tiles
        self._pattern_lines[pattern_line_row][mask_empty_fields] = empty_fields

        return temp_out_of_game_tiles