import numpy as np

class Factory:
    
    def __init__(self) -> None:
        self.tiles = np.array([], dtype=int)

    def get_tiles(self) -> np.ndarray:
        return self.tiles.copy()
    
    def get_and_remove_tiles(self) -> np.ndarray:
        tiles = self.tiles.copy()
        self.tiles = np.array([], dtype=int)
        return tiles

    def get_and_remove_color_tiles(self, color_id: int) -> np.ndarray:
        mask = self.tiles == color_id
        if self.tiles[mask].size > 0:
            # get first player marker
            mask = np.logical_or(self.tiles == color_id, self.tiles == 0)
        tiles = self.tiles[mask]
        self.tiles = self.tiles[~mask]
        return tiles

    def add_tiles(self, tiles: np.ndarray) -> None:
        np.concatenate((self.tiles, tiles))
        np.logical_or()