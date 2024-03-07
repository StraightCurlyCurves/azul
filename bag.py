import numpy as np
from symbols import Symbol

class Bag:

    def __init__(self) -> None:
        self._tiles = np.zeros(100, dtype=int)
        self._tiles[0:20] = Symbol.Color1
        self._tiles[20:40] = Symbol.Color2
        self._tiles[40:60] = Symbol.Color3
        self._tiles[60:80] = Symbol.Color4
        self._tiles[80:] = Symbol.Color5

    def get_and_remove_n_tiles(self, n: int) -> np.ndarray:
        if n > self._tiles.size:
            tiles = self._tiles
            self._tiles = np.array([], dtype=int)
            return tiles
        mask = np.full(self._tiles.size, False, dtype=bool)
        random_indices = np.random.choice(self._tiles.size, n, replace=False)
        mask[random_indices] = True
        tiles = self._tiles[mask]
        self._tiles = self._tiles[~mask]
        return tiles

    def add_tiles(self, tiles) -> None:
        self._tiles = np.concatenate((self._tiles, tiles))