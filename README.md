# Azul
Azul is a boardgame for 2-4 players. With this repository you can play Azul with your friends, against bots or let bots play against each other.

If not set otherwise, a history of the game will be saved. The history can be loaded to go back to a certain point of the game and take a different turn from there.

IMPORTANT: Make sure the console is high enough to display the whole game board. Otherwise the game will not be displayed correctly.

# How to get started
- How to play a game
- How to write a bot

## How to play a game
If you play a game with manual players (not bots) or mixed, the console asks the non-bot players to provide a factory ID to pick from, a color ID to pick and a pattern line row you wish to place the tiles on.

If you place the tiles on a pattern line row which can't hold some or any of the tiles, the corresponding tiles will automatically fall on the floor line.

In case you provided an invalid factory ID or Color ID, it will ask you for it again.

If you mistakenly picked a factory ID or Color ID you didn't whish to pick, provide the letter 'c' to the color ID or pattern line row to cancel your inputs and to start your turn over.

In case you are not happy with your turn or mistyped the last input (pattern line row) you always can go back in history as many times you wish (and your co-players let you) by providing the letter 'b' to the factory ID.

Was the turn okay nevertheless, you can go forward in history by providing the letter 'f' to the factory ID.

Here are some examples on how you can play different kind of games. These examples can also be found in ``play_azul.py``

If you're not in ``play_azul.py``, import ``PlayAzul``:
```python
from play_azul import PlayAzul
```

### Play a game with two friends
```python
players = ['Me', 'Myself', 'I']
game = PlayAzul(players=players)
ranklist = game.play()
for i, rank in enumerate(ranklist):
    print(f'{i+1}. {rank[0]}, Score: {rank[2]}')
```

### Play a game against a bot
```python
bot = MyBot('Bot')
players = ['Me', bot]
game = PlayAzul(players=players)
ranklist = game.play()
for i, rank in enumerate(ranklist):
    print(f'{i+1}. {rank[0]}, Score: {rank[2]}')
```

### Let three bots play against each other
```python
bot_1 = MyBot('Bot 1')
bot_2 = MyBot('Bot 2')
bot_3 = MyBot('Bot 3')
players=[bot_1, bot_2, bot_3]
game = PlayAzul(players=players, history_file_name='bot_game')
ranklist = game.play()
for i, rank in enumerate(ranklist):
    print(f'{i+1}. {rank[0]}, Score: {rank[2]}')
```

### Load a game played by bots but play and alternate it manually
```python
players = ['Me', 'Myself', 'I']
game = PlayAzul(players=players, history='bot_game')
ranklist = game.play()
for i, rank in enumerate(ranklist):
    print(f'{i+1}. {rank[0]}, Score: {rank[2]}')
```

### Simulate 1000 games between two bots
```python
bot_1 = MyBot('Bot 1')
bot_2 = MyBot('Bot 2')
players=[bot_1, bot_2]
game = PlayAzul(players=players, show_bots_move=False, save_history=False)
wins = [0]*len(players)
for i in range(1000):
    ranklist = game.play()
    winner_id = ranklist[0][1]
    wins[winner_id] += 1
    print('\r', end='')
    print(f'{i+1} games played', end='')
print('Wins:', wins)
```

## How to write a bot
Create a bot class by inheriting ``Bot`` from ``bot.py``. Reimplement the ``get_move`` method returning a valid move ``tuple[factory_id, color_id, pattern_line_row]``. The method provides you with the visible state of the game board and which player's turn it is:

- ``factories``: List of all factories. ``factory[0]`` is the middle pool. 
  - Public methods and properties:
    - ``get_and_remove_tiles()``
    - ``get_and_remove_color_tiles(color_id)``
    - ``add_tiles(tiles)``
    - ``tiles``
  
- ``playerboards``: List of all playerboards.
  - Public methods and properties:
    - ``place_tiles(tiles, pattern_line_row)``
    - ``handle_end_of_round_and_get_tiles()``
    - ``handle_end_of_game()``
    - ``score``
    - ``wall``
    - ``wall_colors``
    - ``pattern_lines``
    - ``floor_line``
- ``player_id``: Player's ID to make a move. Its corresponding playerboard is ``playerboard[player_id]``

A simple example ``MyBot`` can be found in ``my_bot.py``. This bot takes the first color of the first valid factory to take tiles from and places it on the first valid pattern line if there is one:

```python
class MyBot(Bot):

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def get_move(self, factories: list[Factory], playerboards: list[Playerboard], player_id: int) -> Move:
        factory_id = None
        color_id = None
        pattern_line_row = None

        # find a valid factory to take tiles from
        for i, factory in enumerate(factories):
            factory_id = i
            tiles = factory.tiles
            valid_tiles_mask = tiles != Symbol.FirstPlayerMarker
            if valid_tiles_mask.any():
                color_id = tiles[valid_tiles_mask][0]
                break
        
        # optional: try to find a valid pattern line to place at least one tile
        playerboard = playerboards[player_id]
        for i, pattern_line in enumerate(playerboard.pattern_lines):
            wall_line = playerboard.wall[i]
            color_not_in_wall_line = color_id not in wall_line
            pattern_line_has_different_color = np.count_nonzero(pattern_line != Symbol.EmptyField) \
                  != np.count_nonzero(pattern_line == color_id)
            pattern_line_is_not_full = np.count_nonzero(pattern_line == Symbol.EmptyField) > 0
            if color_not_in_wall_line and not pattern_line_has_different_color and pattern_line_is_not_full:
                pattern_line_row = i
                break
            else:
                pattern_line_row = -1
            
        return Move(factory_id, color_id, pattern_line_row)
```