from bot import Bot

class Player:

    def __init__(self, player: str|Bot) -> None:
        self.bot = None
        self.is_bot = True if type(player)==Bot else False
        self.name = ''
        if self.is_bot :
            self.bot = player
            self.name = self.bot.get_name()
        else:
            assert type(player) == str
            self.name = player

    

            
