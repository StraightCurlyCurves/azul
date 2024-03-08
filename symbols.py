import numpy as np

class Symbol:
    EmptyField = 0
    Color1 = 1
    Color2 = 2
    Color3 = 3
    Color4 = 4
    Color5 = 5
    FirstPlayerMarker = 6

    def is_valid_color(color_id: int) -> bool:
        valid_colors = np.array([Symbol.Color1,Symbol.Color2,Symbol.Color3,Symbol.Color4,Symbol.Color5])
        return np.count_nonzero(valid_colors==color_id) > 0