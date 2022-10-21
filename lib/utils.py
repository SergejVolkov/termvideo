import os

from time import perf_counter_ns
from colorama import Back

from .cursor import hide_cursor, show_cursor


def perf_counter_ms():
    return perf_counter_ns() // 1000000


def init_terminal():
    if os.name == "nt":
        os.system("")
    hide_cursor()


def reset_terminal():
    print(Back.RESET)
    show_cursor()
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
