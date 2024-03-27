import numpy as np
from symbols import Symbol
from factory import Factory

def test_tiles():
    f = Factory()
    f._tiles = np.array([1,1,2,3], dtype=int)
    tiles = f.tiles
    assert tiles.size == 4
    assert id(tiles) != id(f._tiles)
    tiles = tiles[:1]
    assert f._tiles.size == 4

def test_get_and_remove_tiles():
    f = Factory()
    f._tiles = np.array([1,1,2,3], dtype=int)
    tiles = f.get_and_remove_tiles()
    assert tiles.size == 4
    assert id(tiles) != id(f._tiles)
    tiles = tiles[:1]
    assert f._tiles.size == 0

def test_get_and_remove_color_tiles():
    f = Factory()
    f._tiles = np.array([1,1,2,3], dtype=int)
    tiles = f.get_and_remove_color_tiles(1)
    assert tiles.size == 2
    assert f._tiles.size == 2
    assert np.array_equal(tiles, np.array([1,1], dtype=int))
    assert np.array_equal(f._tiles, np.array([2,3], dtype=int))

def test_get_and_remove_non_existing_color_tiles():
    f = Factory()
    f._tiles = np.array([1,1,2,3], dtype=int)
    tiles = f.get_and_remove_color_tiles(4)
    assert tiles.size == 0
    assert f._tiles.size == 4

    f._tiles = np.array([], dtype=int)
    tiles = f.get_and_remove_color_tiles(4)
    assert tiles.size == 0
    assert f._tiles.size == 0

def test_get_and_remove_color_tiles_with_first_player_marker():
    f = Factory()
    f._tiles = np.array([1,1,2,3,Symbol.FirstPlayerMarker], dtype=int)
    tiles = f.get_and_remove_color_tiles(1)
    assert tiles.size == 3
    assert f._tiles.size == 2
    assert np.array_equal(tiles, np.array([1,1,Symbol.FirstPlayerMarker], dtype=int))
    assert np.array_equal(f._tiles, np.array([2,3], dtype=int))

def test_get_and_remove_non_existing_color_tiles_with_first_player_marker():
    f = Factory()
    f._tiles = np.array([1,1,2,3,Symbol.FirstPlayerMarker], dtype=int)
    tiles = f.get_and_remove_color_tiles(4)
    assert tiles.size == 0
    assert f._tiles.size == 5

def test_add_tiles():
    f = Factory()
    tiles = np.array([1,1,2,3], dtype=int)
    f.add_tiles(tiles)
    assert f._tiles.size == 4
    f.add_tiles(tiles)
    assert f._tiles.size == 8