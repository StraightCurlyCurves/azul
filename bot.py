from abc import ABC, abstractmethod

from factory import Factory
from playerboard import Playerboard

from move import Move

class Bot(ABC):

    def __init__(self, name: str) -> None:
        self._name = name

    @abstractmethod
    def get_move(self, factories: list[Factory], playerboards: list[Playerboard], player_id: int) -> Move:
        pass
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
        