import numpy as np



class Bag:

    def __init__(self) -> None:
        self._tiles = np.zeros(100)
        self._tiles[0:20] = 1
        self._tiles[20:40] = 2
        self._tiles[40:60] = 3
        self._tiles[60:80] = 4
        self._tiles[80:] = 5

    def get_and_remove_n_tiles(self, n: int) -> np.ndarray:
        mask = np.full(self._tiles.size, False, dtype=bool)
        random_indices = np.random.choice(self._tiles.size, n)
        mask[random_indices] = True
        tiles = self._tiles[mask]
        self._tiles = self._tiles[~mask]
        return tiles

    def add_tiles(self, tiles):
        self._tiles = np.concatenate((self._tiles, tiles))