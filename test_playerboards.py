import numpy as np
import pytest
from symbols import Symbol
from playerboard import Playerboard

EF = Symbol.EmptyField
C1 = Symbol.Color1
C2 = Symbol.Color2
C3 = Symbol.Color3
C4 = Symbol.Color4
C5 = Symbol.Color5
FPM = Symbol.FirstPlayerMarker

def test_place_tiles_on_floor_line():
    pb = Playerboard()
    tiles = np.array([C1,C2,C3,C4], dtype=int)
    temp_out_of_game_tiles = pb._place_tiles_on_floor_line(tiles)
    assert temp_out_of_game_tiles.size == 0

    tiles = np.array([C1,C2,C3,C4], dtype=int)
    temp_out_of_game_tiles = pb._place_tiles_on_floor_line(tiles)
    assert np.array_equal(pb._floor_line, np.array([C1,C2,C3,C4,C1,C2,C3], dtype=int))
    assert np.array_equal(temp_out_of_game_tiles, np.array([C4], dtype=int))

    tiles = np.array([C3,C3,FPM,C4], dtype=int)
    temp_out_of_game_tiles = pb._place_tiles_on_floor_line(tiles)
    assert np.array_equal(pb._floor_line, np.array([FPM,C2,C3,C4,C1,C2,C3], dtype=int))
    assert np.array_equal(temp_out_of_game_tiles, np.array([C1,C3,C3,C4], dtype=int))

def test_place_tiles_on_pattern_line():
    pb = Playerboard()
    tiles = np.array([C3,C3,C3,C3], dtype=int)

    temp_out_of_game_tiles = pb._place_tiles_on_pattern_line(tiles, 2)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._floor_line, np.array([C3, *[EF]*6], dtype=int))
    assert np.array_equal(pb._pattern_lines[2], np.array([C3,C3,C3], dtype=int))

    temp_out_of_game_tiles = pb._place_tiles_on_pattern_line(tiles, 3)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._floor_line, np.array([C3, *[EF]*6], dtype=int))
    assert np.array_equal(pb._pattern_lines[3], np.array([C3,C3,C3,C3], dtype=int))

    temp_out_of_game_tiles = pb._place_tiles_on_pattern_line(tiles, 4)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._floor_line, np.array([C3, *[EF]*6], dtype=int))
    assert np.array_equal(pb._pattern_lines[4], np.array([EF,C3,C3,C3,C3], dtype=int))

    temp_out_of_game_tiles = pb._place_tiles_on_pattern_line(tiles, 0)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._floor_line, np.array([C3,C3,C3,C3,EF,EF,EF], dtype=int))
    assert np.array_equal(pb._pattern_lines[0], np.array([C3], dtype=int))

    temp_out_of_game_tiles = pb._place_tiles_on_pattern_line(tiles, 0)
    assert temp_out_of_game_tiles.size == 1
    assert np.array_equal(pb._floor_line, np.array([C3]*7, dtype=int))
    assert np.array_equal(pb._pattern_lines[0], np.array([C3], dtype=int))
    
    tiles = np.array([], dtype=int)
    with pytest.raises(AssertionError):
        pb._place_tiles_on_pattern_line(tiles, 4)

    tiles = np.array([C3,C3,FPM], dtype=int)
    with pytest.raises(AssertionError):
        pb._place_tiles_on_pattern_line(tiles, 4)

def test_place_tiles():
    pb = Playerboard()
    tiles = np.array([C3,C3,C3,C3], dtype=int)

    temp_out_of_game_tiles = pb.place_tiles(tiles, 4)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._pattern_lines[4], np.array([EF,C3,C3,C3,C3], dtype=int))
    assert np.array_equal(pb._floor_line, np.array([EF]*7, dtype=int))

    temp_out_of_game_tiles = pb.place_tiles(tiles, 4)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._pattern_lines[4], np.array([C3,C3,C3,C3,C3], dtype=int))
    assert np.array_equal(pb._floor_line, np.array([C3,C3,C3,EF,EF,EF,EF], dtype=int))

    temp_out_of_game_tiles = pb.place_tiles(tiles, 3)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._pattern_lines[3], np.array([C3,C3,C3,C3], dtype=int))
    assert np.array_equal(pb._floor_line, np.array([C3,C3,C3,EF,EF,EF,EF], dtype=int))

    tiles = np.array([C3,C3,C4], dtype=int)
    with pytest.raises(AssertionError):
        temp_out_of_game_tiles = pb.place_tiles(tiles, 2)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._pattern_lines[2], np.array([EF,EF,EF], dtype=int))
    assert np.array_equal(pb._floor_line, np.array([C3,C3,C3,EF,EF,EF,EF], dtype=int))

    tiles = np.array([C3,C3,FPM], dtype=int)
    temp_out_of_game_tiles = pb.place_tiles(tiles, 1)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._pattern_lines[1], np.array([C3,C3], dtype=int))
    assert np.array_equal(pb._floor_line, np.array([C3,C3,C3,FPM,EF,EF,EF], dtype=int))

    pb = Playerboard()
    pb._floor_line[:6] = C4
    tiles = np.array([C2,C2,FPM], dtype=int)
    temp_out_of_game_tiles = pb.place_tiles(tiles, 0)
    assert temp_out_of_game_tiles.size == 1
    assert np.array_equal(temp_out_of_game_tiles, np.array([C2], dtype=int))
    assert np.array_equal(pb._pattern_lines[0], np.array([C2], dtype=int))
    assert np.array_equal(pb._floor_line, np.array([C4,C4,C4,C4,C4,C4,FPM], dtype=int))

    pb = Playerboard()
    pb._floor_line[:7] = C4
    tiles = np.array([C2,C2,FPM], dtype=int)
    temp_out_of_game_tiles = pb.place_tiles(tiles, 0)
    assert temp_out_of_game_tiles.size == 2
    assert np.array_equal(temp_out_of_game_tiles, np.array([C4, C2], dtype=int))
    assert np.array_equal(pb._pattern_lines[0], np.array([C2], dtype=int))
    assert np.array_equal(pb._floor_line, np.array([FPM,C4,C4,C4,C4,C4,C4], dtype=int))

    pb = Playerboard()
    tiles = np.array([C2,C2], dtype=int)
    temp_out_of_game_tiles = pb.place_tiles(tiles, -1)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._floor_line, np.array([C2,C2,EF,EF,EF,EF,EF], dtype=int))

    tiles = np.array([C3,C3,FPM], dtype=int)
    temp_out_of_game_tiles = pb.place_tiles(tiles, -1)
    assert temp_out_of_game_tiles.size == 0
    assert np.array_equal(pb._floor_line, np.array([C2,C2,FPM,C3,C3,EF,EF], dtype=int))

    # test if wall_line_has_color
    pb = Playerboard()
    _ = pb._place_tile_on_wall_and_count_points(C1,1)
    assert np.count_nonzero(pb._pattern_lines[1]==EF) == 2
    tiles = np.array([C1,C1], dtype=int)
    _ = pb.place_tiles(tiles, 1)
    assert np.count_nonzero(pb._pattern_lines[1]==EF) == 2
    assert np.array_equal(pb._floor_line, np.array([C1,C1,EF,EF,EF,EF,EF], dtype=int))

    # test pattern_line_has_different_color
    pb = Playerboard()
    tiles = np.array([C1], dtype=int)
    _ = pb.place_tiles(tiles, 1)
    assert np.count_nonzero(pb._pattern_lines[1]==C1) == 1
    assert np.array_equal(pb._floor_line, np.array([EF,EF,EF,EF,EF,EF,EF], dtype=int))
    tiles = np.array([C2], dtype=int)
    _ = pb.place_tiles(tiles, 1)
    assert np.count_nonzero(pb._pattern_lines[1]==C1) == 1
    assert np.array_equal(pb._floor_line, np.array([C2,EF,EF,EF,EF,EF,EF], dtype=int))

def test_place_tile_on_wall_and_count_points():
    pb = Playerboard()
    end_of_game = pb._place_tile_on_wall_and_count_points(C2,0)
    assert end_of_game == False
    assert pb._score == 1

    end_of_game = pb._place_tile_on_wall_and_count_points(C3,0)
    assert end_of_game == False
    assert pb._score == 3

    end_of_game = pb._place_tile_on_wall_and_count_points(C1,1)
    assert end_of_game == False
    assert pb._score == 5

    end_of_game = pb._place_tile_on_wall_and_count_points(C2,1)
    assert end_of_game == False
    assert pb._score == 9

    end_of_game = pb._place_tile_on_wall_and_count_points(C5,2)
    assert end_of_game == False
    assert pb._score == 12

    end_of_game = pb._place_tile_on_wall_and_count_points(C3,4)
    assert end_of_game == False
    assert pb._score == 13

    end_of_game = pb._place_tile_on_wall_and_count_points(C4,3)
    assert end_of_game == False
    assert pb._score == 18

    end_of_game = pb._place_tile_on_wall_and_count_points(C4,4)
    assert end_of_game == False
    assert pb._score == 20

    end_of_game = pb._place_tile_on_wall_and_count_points(C1,4)
    assert end_of_game == False
    assert pb._score == 21

    end_of_game = pb._place_tile_on_wall_and_count_points(C5,4)
    assert end_of_game == False
    assert pb._score == 25

    end_of_game = pb._place_tile_on_wall_and_count_points(C2,4)
    assert end_of_game == True
    assert pb._score == 30

def test_handle_end_of_round_and_get_tiles():
    pb = Playerboard()
    pb._floor_line[:3] = [C2,C3,C4]
    end_of_game = pb._place_tile_on_wall_and_count_points(C2,0)
    end_of_game = pb._place_tile_on_wall_and_count_points(C3,0)
    end_of_game = pb._place_tile_on_wall_and_count_points(C1,1)
    end_of_game = pb._place_tile_on_wall_and_count_points(C2,1)
    end_of_game = pb._place_tile_on_wall_and_count_points(C5,2)
    end_of_game = pb._place_tile_on_wall_and_count_points(C3,4)
    end_of_game = pb._place_tile_on_wall_and_count_points(C4,3)
    end_of_game = pb._place_tile_on_wall_and_count_points(C4,4)
    end_of_game = pb._place_tile_on_wall_and_count_points(C1,4)
    end_of_game = pb._place_tile_on_wall_and_count_points(C5,4)
    assert end_of_game == False
    assert pb._score == 25

    tiles = np.array([C1], dtype=int)
    pb._place_tiles_on_pattern_line(tiles, 0)
    assert pb._score == 25

    tiles = np.array([C3], dtype=int)
    pb._place_tiles_on_pattern_line(tiles, 1)
    assert pb._score == 25

    tiles = np.array([C4,C4,C4], dtype=int)
    pb._place_tiles_on_pattern_line(tiles, 2)
    assert pb._score == 25

    is_end_of_game, tiles = pb.handle_end_of_round_and_get_tiles()
    assert is_end_of_game == False
    assert tiles.size == 5
    assert pb._score == 26

def test_handle_end_of_game():
    pb = Playerboard()
    pb._floor_line[:3] = [C2,C3,C4]
    end_of_game = pb._place_tile_on_wall_and_count_points(C1,0)
    end_of_game = pb._place_tile_on_wall_and_count_points(C1,1)
    end_of_game = pb._place_tile_on_wall_and_count_points(C1,2)
    end_of_game = pb._place_tile_on_wall_and_count_points(C1,3)
    end_of_game = pb._place_tile_on_wall_and_count_points(C1,4)
    end_of_game = pb._place_tile_on_wall_and_count_points(C2,0)
    end_of_game = pb._place_tile_on_wall_and_count_points(C5,2)
    end_of_game = pb._place_tile_on_wall_and_count_points(C4,3)
    end_of_game = pb._place_tile_on_wall_and_count_points(C3,4)
    end_of_game = pb._place_tile_on_wall_and_count_points(C3,0)
    end_of_game = pb._place_tile_on_wall_and_count_points(C2,1)
    end_of_game = pb._place_tile_on_wall_and_count_points(C5,3)
    end_of_game = pb._place_tile_on_wall_and_count_points(C4,4)
    end_of_game = pb._place_tile_on_wall_and_count_points(C5,4)
    assert end_of_game == False
    assert pb._score == 51

    tiles = np.array([C3], dtype=int)
    pb._place_tiles_on_pattern_line(tiles, 1)
    assert pb._score == 51

    tiles = np.array([C2,C2,C2,C2,C2], dtype=int)
    pb._place_tiles_on_pattern_line(tiles, 4)
    assert pb._score == 51

    is_end_of_game, tiles = pb.handle_end_of_round_and_get_tiles()
    assert is_end_of_game == True
    assert tiles.size == 7
    assert pb._score == 52

    score = pb.handle_end_of_game()
    assert score == 52 + 26
