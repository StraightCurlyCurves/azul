import numpy as np
from symbols import Symbol
from factory import Factory
from playerboard import Playerboard


class Bot:

    def __init__(self) -> None:
        pass

    def get_move(self, factories: list[Factory], playerboards: list[Playerboard]):
        factory_id: int = 0
        color_id: int = 0
        pattern_line_row: int = 0

        return factory_id, color_id, pattern_line_row