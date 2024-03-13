import numpy as np

from azul import Azul


if __name__ == '__main__':
    player_count = 2
    load_history = False
    history_path = 'history_2024-03-13_15-56-10_2_player_seed_8665.npy'

    if load_history:
        player_count = int(history_path.split('_')[-4])
        # not really necessary, but will lead to same outcome if newly played the same
        seed = int(history_path.split('_')[-1].split('.')[0])
    else:
        seed = np.random.randint(100000)
    np.random.seed(seed)

    first_player_id = np.random.randint(player_count)

    a = Azul(player_count, first_player_id)
    if load_history:
        a.load_history(history_path)
    is_end_of_game = False
    is_end_of_round = False
    
    while not is_end_of_game:
        a.print_state()

        factory_id = input(f'Factory ID: ')
        if factory_id == 'b':
            a.move_back()
            continue
        elif factory_id == 'f':
            a.move_forward()
            continue
        elif factory_id == 'q':
            a.save_history(seed)
            print('Saved game and quit.')
            break
        else:
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
        
        if is_end_of_game:
            a.print_state()
            console_input = input("End of game. Press Enter to save and quit or 'b' to go back one move.")
            if console_input == 'b':
                a.move_back()
                is_end_of_game = False
            else:
                a.save_history(seed)