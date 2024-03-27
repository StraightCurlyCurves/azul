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
    print(f'{Colors.fpm}First Player Marker{Colors.reset}')
    print(f'{Colors.ef}Empty Field{Colors.reset}')
    print(f'{Colors.c1}Color 1{Colors.reset}')
    print(f'{Colors.c2}Color 2{Colors.reset}')
    print(f'{Colors.c3}Color 3{Colors.reset}')
    print(f'{Colors.c4}Color 4{Colors.reset}')
    print(f'{Colors.c5}Color 5{Colors.reset}')
    print(f'{Colors.bg_fpm}   {Colors.reset}')
    print(f'{Colors.bg_ef}   {Colors.reset}')
    print(f'{Colors.bg_c1}   {Colors.reset}')
    print(f'{Colors.bg_c2}   {Colors.reset}')
    print(f'{Colors.bg_c3}   {Colors.reset}')
    print(f'{Colors.bg_c4}   {Colors.reset}')
    print(f'{Colors.bg_c5}   {Colors.reset}')
    print(f'{Colors.underline}underline{Colors.reset}')
    print(f'{Colors.italic}italic{Colors.reset}')
    print(f'{Colors.underline}{Colors.italic}italic underline{Colors.reset}')