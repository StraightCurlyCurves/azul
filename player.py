from copy import deepcopy
from bot import Bot

class Player:

    def __init__(self, player: str|Bot, player_id: int) -> None:
        self._bot = None
        self._is_bot = isinstance(player, Bot)
        self._name = ''
        self._player_id = player_id
        if self._is_bot :
            self._bot = player
            self._name = self._bot.name
        else:
            assert type(player) == str
            self._name = player

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def player_id(self) -> int:
        return self._player_id
    
    @property
    def is_bot(self) -> bool:
        return self._is_bot
    
    @property
    def bot(self) -> Bot:
        return deepcopy(self._bot)
    