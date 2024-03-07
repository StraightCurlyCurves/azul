import numpy as np
from symbols import Symbol
from bag import Bag

def test_init():
    b = Bag()
    assert b._tiles.size == 100
    assert np.count_nonzero(b._tiles==Symbol.Color1) == 20
    assert np.count_nonzero(b._tiles==Symbol.Color2) == 20
    assert np.count_nonzero(b._tiles==Symbol.Color3) == 20
    assert np.count_nonzero(b._tiles==Symbol.Color4) == 20
    assert np.count_nonzero(b._tiles==Symbol.Color5) == 20

def test_get_and_remove_n_tiles():
    b = Bag()
    tiles = b.get_and_remove_n_tiles(50)
    assert tiles.size + b._tiles.size == 100
    assert tiles.size == 50
    assert b._tiles.size == 50
    tiles = b.get_and_remove_n_tiles(50)
    assert tiles.size == 50
    assert b._tiles.size == 0

    b = Bag()
    tiles = b.get_and_remove_n_tiles(104)
    assert tiles.size == 100
    assert b._tiles.size == 0
    tiles = b.get_and_remove_n_tiles(10)
    assert tiles.size == 0
    assert b._tiles.size == 0
    assert type(tiles) == np.ndarray

def test_add_tiles():
    b = Bag()
    size = b._tiles.size
    tiles = b.get_and_remove_n_tiles(20)
    b.add_tiles(tiles)
    assert b._tiles.size == size