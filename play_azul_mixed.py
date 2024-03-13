import numpy as np

from bot import Bot
from azul import Azul


if __name__ == '__main__':
    players = [Bot(), 'human']
    player_count = len(players)

    seed = np.random.randint(100000)
    np.random.seed(seed)
    first_player_id=np.random.randint(player_count)

    a = Azul(player_count, first_player_id)

    is_end_of_game = False

    while not is_end_of_game:
        a.print_state()

        player = players[a._players_move]
        if  player== 'human':
            factory_id = input(f'Factory ID: ')
            if factory_id == 'q':
                a.save_history(seed)
                print('Saved game and quit.')
                break         
            try:
                factory_id = int(factory_id)
            except:
                input('Not a valid input. Press Enter to try again.')
                continue

            color_id = input(f'Color ID: ')
            if color_id == 'c': continue  
            else:
                try:
                    color_id = int(color_id)
                except:
                    input('Not a valid input. Press Enter to try again.')
                    continue

            pattern_line_row = input(f'Pattern line row: ')
            if pattern_line_row == 'c': continue
            else:
                try:
                    pattern_line_row = int(pattern_line_row)
                except:
                    input('Not a valid input. Press Enter to try again.')
                    continue

            try:
                is_end_of_game = a.make_move(factory_id, color_id, pattern_line_row, player_id=a._players_move)
            except Exception as e:
                print(repr(e))
                input('Press Enter to try again.')
                continue
        else:
            player: Bot
            move = player.get_move(a.get_factories(), a.get_playerboards())
            try:
                is_end_of_game = a.make_move(*move, a._players_move)
            except Exception as e:
                print(repr(e))
                input(f'Bot with player ID {a._players_move} messed up.')
                exit()

        if is_end_of_game:
            a.print_state()
            a.save_history(seed)
            print("End of game. Game saved.")