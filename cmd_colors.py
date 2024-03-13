class Colors:    
    fpm = '\033[38;5;226m'
    ef = '\033[90m'
    c1 = '\033[38;5;196m'
    c2 = '\033[38;5;2m'
    c3 = '\033[38;5;208m'
    c4 = '\033[38;5;4m'
    c5 = '\033[38;5;164m'
    bg_fpm = '\033[48;5;221m'
    bg_ef = '\033[100m'
    bg_c1 = '\033[104m'
    bg_c2 = '\033[48;5;208m'
    bg_c3 = '\033[48;5;170m'
    bg_c4 = '\033[48;5;78m'
    bg_c5 = '\033[48;5;203m'
    bg_green = '\033[48;5;70m'
    underline = '\033[4m'
    italic = '\033[3m'
    bold = '\033[1m'
    white = '\033[97m'
    black = '\033[30m'
    reset = '\033[0m'
    colors = [fpm, ef, c1, c2, c3, c4, c5, bg_fpm, bg_ef, bg_c1, bg_c2, bg_c3, bg_c4, bg_c5, bg_green,
              underline, italic, bold, white, black, reset]
    
if __name__ == '__main__':
    # for i, color in enumerate(bcolors.colors):
    #     print(f'{i}: {color}Test color ...{bcolors.colors[-1]}')
    print(f'{Colors.colors[0]}First Player Marker{Colors.colors[-1]}')
    print(f'{Colors.colors[1]}Empty Field{Colors.colors[-1]}')
    print(f'{Colors.colors[2]}Color 1{Colors.colors[-1]}')
    print(f'{Colors.colors[3]}Color 2{Colors.colors[-1]}')
    print(f'{Colors.colors[4]}Color 3{Colors.colors[-1]}')
    print(f'{Colors.colors[5]}Color 4{Colors.colors[-1]}')
    print(f'{Colors.colors[6]}Color 5{Colors.colors[-1]}')
    print(f'{Colors.colors[7]}   {Colors.colors[-1]}')
    print(f'{Colors.colors[8]}   {Colors.colors[-1]}')
    print(f'{Colors.colors[9]}   {Colors.colors[-1]}')
    print(f'{Colors.colors[10]}   {Colors.colors[-1]}')
    print(f'{Colors.colors[11]}   {Colors.colors[-1]}')
    print(f'{Colors.colors[12]}   {Colors.colors[-1]}')
    print(f'{Colors.colors[13]}   {Colors.colors[-1]}')
    print(f'{Colors.colors[14]}underline{Colors.colors[-1]}')
    print(f'{Colors.colors[15]}italic{Colors.colors[-1]}')
    print(f'{Colors.colors[14]}{Colors.colors[15]}italic underline{Colors.colors[-1]}')