"""
Filename: _colorful_text.py
Description: This file defines functionality to bring colors to the console.

Author: TravisGK
Version: 1.0

License: GNU License
"""

# the program doesn't require colorama
# but could support the consoles on older versions of Windows.
_colorama_loaded = True
try:
    import colorama

    colorama.just_fix_windows_console()
except ModuleNotFoundError:
    _colorama_loaded = False


def fore_color(color: str = "reset"):
    """Returns an embedding that when printed changes the console color."""
    if _colorama_loaded:
        code = {
            "black": colorama.Fore.BLACK,
            "red": colorama.Fore.RED,
            "green": colorama.Fore.GREEN,
            "yellow": colorama.Fore.YELLOW,
            "blue": colorama.Fore.BLUE,
            "magenta": colorama.Fore.MAGENTA,
            "cyan": colorama.Fore.CYAN,
            "white": colorama.Fore.WHITE,
        }.get(color)
        return colorama.Fore.RESET if code is None else code

    code = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }.get(color)
    return "\033[0m" if code is None else code
