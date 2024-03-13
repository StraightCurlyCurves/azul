class Colors:
    # colors = ['\033[97m',
    #         '\033[40m',
    #         '\033[38;5;144m', # TITLE = '\033[38;5;144m'
    #         '\033[38;2;170;185;89m',     # TITLE = '\033[38;2;170;185;89m'
    #         '\033[38;5;80m',     # SECTION = '\033[38;5;80m'
    #         5'\033[38;5;170m',     # HEADER = '\033[38;5;170m'
    #         '\033[38;5;208m',     # TTIME = '\033[38;5;208m'
    #         '\033[30m',     # BLACK = '\033[30m'
    #         '\033[38;5;15m',     # WHITE = '\033[38;5;15m'
    #         '\033[38;5;245m',     # GREY = '\033[38;5;245m'
    #         10'\033[90m',     # BRIGHT_BLACK = '\033[90m'
    #         '\033[94m',     # OKBLUE = '\033[94m'
    #         '\033[38;5;75m',     # OKCYAN = '\033[38;5;75m'
    #         '\033[38;5;78m',     # OKGREEN = '\033[38;5;78m'
    #         '\033[38;5;221m',     # WARNING = '\033[38;5;221m'
    #         15'\033[38;5;203m',     # FAIL = '\033[38;5;203m'
    #         '\033[1m',     # ENDC = f'{fg_color}{bg_color}'
    #         '\033[4m',     # BOLD = '\033[1m'
    #         '\033[48;5;80m',
    #         '\033[38;5;80m',   
    #         '\033[0m']     # reset

    
    fpm = '\033[38;5;221m'
    ef = '\033[90m'
    c1 = '\033[94m'
    c2 = '\033[38;5;208m'
    c3 = '\033[38;5;170m'
    c4 = '\033[38;5;78m'
    c5 = '\033[38;5;203m'
    bg_fpm = '\033[48;5;221m'
    bg_ef = '\033[100m'
    bg_c1 = '\033[104m'
    bg_c2 = '\033[48;5;208m'
    bg_c3 = '\033[48;5;170m'
    bg_c4 = '\033[48;5;78m'
    bg_c5 = '\033[48;5;203m'
    underline = '\033[4m'
    italic = '\033[3m'
    reset = '\033[0m'
    colors = [fpm, ef, c1, c2, c3, c4, c5, bg_fpm, bg_ef, bg_c1, bg_c2, bg_c3, bg_c4, bg_c5, underline, italic, reset]
    
if __name__ == '__main__':
    # for i, color in enumerate(bcolors.colors):
    #     print(f'{i}: {color}Test color ...{bcolors.colors[-1]}')
    print(f'{bcolors.colors[0]}First Player Marker{bcolors.colors[-1]}')
    print(f'{bcolors.colors[1]}Empty Field{bcolors.colors[-1]}')
    print(f'{bcolors.colors[2]}Color 1{bcolors.colors[-1]}')
    print(f'{bcolors.colors[3]}Color 2{bcolors.colors[-1]}')
    print(f'{bcolors.colors[4]}Color 3{bcolors.colors[-1]}')
    print(f'{bcolors.colors[5]}Color 4{bcolors.colors[-1]}')
    print(f'{bcolors.colors[6]}Color 5{bcolors.colors[-1]}')
    print(f'{bcolors.colors[7]}   {bcolors.colors[-1]}')
    print(f'{bcolors.colors[8]}   {bcolors.colors[-1]}')
    print(f'{bcolors.colors[9]}   {bcolors.colors[-1]}')
    print(f'{bcolors.colors[10]}   {bcolors.colors[-1]}')
    print(f'{bcolors.colors[11]}   {bcolors.colors[-1]}')
    print(f'{bcolors.colors[12]}   {bcolors.colors[-1]}')
    print(f'{bcolors.colors[13]}   {bcolors.colors[-1]}')
    print(f'{bcolors.colors[14]}underline{bcolors.colors[-1]}')
    print(f'{bcolors.colors[15]}italic{bcolors.colors[-1]}')
    print(f'{bcolors.colors[14]}{bcolors.colors[15]}italic underline{bcolors.colors[-1]}')