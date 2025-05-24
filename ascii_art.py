import os
from utils import *
ASCII_ART_DIR = os.path.join('data', 'ascii_art')

def slow_print_art(filename):
    """
    slow_print the ASCII art from a file in data/ascii_art/.
    :param filename: str - Name of the ASCII art file (e.g. 'void.txt')
    """
    path = os.path.join(ASCII_ART_DIR, filename)
    #slow_print(f"DEBUG: Attempting to open ASCII art file at: {path}")
    try:
        with open(path, 'r', encoding='utf-8') as file:
            art = file.read()
            slow_print(art)
    except FileNotFoundError:
        print(f"[ASCII Art file '{filename}' not found at {path}]")

