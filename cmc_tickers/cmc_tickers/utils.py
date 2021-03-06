from fabric.colors import _wrap_with
from colorama import init # pip install colorama
from colorama import Fore, Back, Style

FORE_COLOR_YELLOW = Fore.YELLOW
FORE_COLOR_GREEN = Fore.GREEN
FORE_COLOR_RED = Fore.RED

FORE_COLOR_BLUE = Fore.BLUE
FORE_COLOR_WHITE = Fore.WHITE
FORE_COLOR_CYAN = Fore.CYAN
FORE_COLOR_MAGENTA = Fore.MAGENTA

def percent_between_numbers(n, min, max):
    if max != None and min != None and n != None:
        d = max - min
        if d != 0:
            return int((n-min) / d * 100)
        else:
            return None
    else:
        return None


def color_blue(msg):
    return color_text (msg, which_color = FORE_COLOR_BLUE)

def color_green(msg):
    return color_text (msg, which_color = FORE_COLOR_GREEN)

def color_red(msg):
    return color_text (msg, which_color = FORE_COLOR_RED)

def color_number_above_below(number, border_value=0, reverse_coloring=False):
    if number != None:
        if number > border_value:
            return color_green(number) if not reverse_coloring else color_red(number)
        elif number < border_value:
            return color_red(number) if not reverse_coloring else color_green(number)
        else:
            return number
    else:
        return number

def color_text (msg, which_color = FORE_COLOR_BLUE):
    try:
        from colorama import init # pip install colorama
        from colorama import Fore, Back, Style

        init()
    except:
        raise ValueError('colorama is not installed, cannot support colored text')
        pass

    try:
        return which_color + str(msg) + Style.RESET_ALL# back to normal color now

    except IOError as e: # avoid "sys.stdout access restricted by mod_wsgi"
        pass

    except:
        raise ValueError(msg)

