import numpy as np
import pytest

from playerboard import Playerboard
from factory import Factory
from bag import Bag
from bot import Bot
from symbols import Symbol
from azul import Azul

EF = Symbol.EmptyField
C1 = Symbol.Color1
C2 = Symbol.Color2
C3 = Symbol.Color3
C4 = Symbol.Color4
C5 = Symbol.Color5
FPM = Symbol.FirstPlayerMarker

np.random.seed(0)

def test_make_move():
    a = Azul()
    ''' with seed(0), color id from Symbol:
    [6]
    [1 2 3 5]
    [1 3 5 5]
    [2 2 4 5]
    [2 2 3 4]
    [1 3 5 5]
    '''
    f_id, c_id, plr, p_id = 2, C5, 1, 0
    is_end_of_round = a.make_move(f_id, c_id, plr, p_id)
    assert is_end_of_round == False
    assert a._factories[f_id]._tiles.size == 0
    assert np.array_equal(a._playerboards[p_id]._pattern_lines[plr], np.array([5,5]))

    f_id, c_id, plr, p_id = 2, C3, 3, 1
    with pytest.raises(Exception):
       is_end_of_round = a.make_move(f_id, c_id, plr, p_id)
    assert a._factories[f_id]._tiles.size == 0
    assert np.array_equal(a._playerboards[p_id]._pattern_lines[plr], np.array([0,0,0,0]))

    f_id, c_id, plr, p_id = 3, C2, 3, 0
    is_end_of_round = a.make_move(f_id, c_id, plr, p_id)
    assert a._factories[f_id]._tiles.size == 0
    assert a._factories[0]._tiles.size == 5
    assert np.array_equal(a._playerboards[p_id]._pattern_lines[plr], np.array([0,0,2,2]))
