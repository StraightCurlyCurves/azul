import numpy as np
from symbols import Symbol
from playerboard import Playerboard

def test_place_tiles_on_floor_line():
    pb = Playerboard()
    tiles = np.array([1,2,3,4], dtype=int)
    temp_out_of_game_tiles = pb._place_tiles_on_floor_line(tiles)
    assert temp_out_of_game_tiles.size == 0

    tiles = np.array([1,2,3,4], dtype=int)
    temp_out_of_game_tiles = pb._place_tiles_on_floor_line(tiles)
    assert np.array_equal(pb._floor_line, np.array([1,2,3,4,1,2,3], dtype=int))
    assert np.array_equal(temp_out_of_game_tiles, np.array([4], dtype=int))

    tiles = np.array([3,3,Symbol.FirstPlayerMarker,4], dtype=int)
    temp_out_of_game_tiles = pb._place_tiles_on_floor_line(tiles)
    assert np.array_equal(pb._floor_line, np.array([Symbol.FirstPlayerMarker,2,3,4,1,2,3], dtype=int))
    assert np.array_equal(temp_out_of_game_tiles, np.array([1,3,3,4], dtype=int))

def test_place_tiles_on_pattern_line():
    pb = Playerboard()
    tiles = np.array([3,3,3,3], dtype=int)

    temp_out_of_game_tiles = pb._place_tiles_on_pattern_line(tiles, 2)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._floor_line, np.array([3, *[0]*6], dtype=int))
    assert np.array_equal(pb._pattern_lines[2], np.array([3,3,3], dtype=int))

    temp_out_of_game_tiles = pb._place_tiles_on_pattern_line(tiles, 3)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._floor_line, np.array([3, *[0]*6], dtype=int))
    assert np.array_equal(pb._pattern_lines[3], np.array([3,3,3,3], dtype=int))

    temp_out_of_game_tiles = pb._place_tiles_on_pattern_line(tiles, 4)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._floor_line, np.array([3, *[0]*6], dtype=int))
    assert np.array_equal(pb._pattern_lines[4], np.array([0,3,3,3,3], dtype=int))

    temp_out_of_game_tiles = pb._place_tiles_on_pattern_line(tiles, 0)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._floor_line, np.array([3,3,3,3, *[0]*3], dtype=int))
    assert np.array_equal(pb._pattern_lines[0], np.array([3], dtype=int))

    temp_out_of_game_tiles = pb._place_tiles_on_pattern_line(tiles, 0)
    assert temp_out_of_game_tiles.size == 1
    assert np.array_equal(pb._floor_line, np.array([3]*7, dtype=int))
    assert np.array_equal(pb._pattern_lines[0], np.array([3], dtype=int))