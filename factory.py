import numpy as np
from symbols import Symbol

class Factory:
    
    def __init__(self) -> None:
        self._tiles = np.array([], dtype=int)
    
    def get_and_remove_tiles(self) -> np.ndarray:
        tiles = self._tiles.copy()
        self._tiles = np.array([], dtype=int)
        return tiles

    def get_and_remove_color_tiles(self, color_id: int) -> np.ndarray:
        mask = self._tiles == color_id
        if self._tiles[mask].size > 0:
            # get first player marker
            mask = np.logical_or(self._tiles == color_id, self._tiles == Symbol.FirstPlayerMarker)
        tiles = self._tiles[mask]
        self._tiles = self._tiles[~mask]
        return tiles

    def add_tiles(self, tiles: np.ndarray) -> None:
        self._tiles = np.concatenate((self._tiles, tiles))

    @property
    def tiles(self) -> np.ndarray:
        return self._tiles.copy()