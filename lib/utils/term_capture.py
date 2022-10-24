import os
import sys
import subprocess
from colorama import Back, Fore

from .cursor import hide_cursor, show_cursor


class term_capture:
    """
    Context manager that configures terminal for playing video.

    On Windows, ASCII escape codes are enabled first.
    Then the cursor is hidden and the terminal window is resized
    to the specified size.

    Args:
        columns (int): Width of the terminal window in characters.
        lines (int): Height of the terminal window in characters.
        clear (bool): Clear the terminal on exit. Defaults to True.

    """

    def __init__(self, columns, lines, clear = True):
        self.columns = columns
        self.lines = lines
        self.clear = clear

        term_size = os.get_terminal_size()
        self.restore_columns = term_size.columns
        self.restore_lines = term_size.lines

    def __enter__(self):
        if os.name == "nt":
            # Enable escape codes use for Windows
            os.system("")

            # Hide cursor
            hide_cursor()

            # Resize the terminal window
            os.system(f"mode {self.columns},{self.lines}")
        else:
            # Hide cursor
            hide_cursor()

            # Resize the terminal window
            sys.stdout.write(f"\033[8;{self.lines};{self.columns}t")
            sys.stdout.flush()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Reset foreground color
        sys.stdout.write(Back.RESET + Fore.RESET)
        sys.stdout.flush()

        # Show cursor
        show_cursor()

        # Clear terminal
        if os.name == "nt":
            subprocess.run(["bin/consize",
                            str(self.restore_columns),
                            str(self.restore_lines),
                            str(self.restore_columns),
                            "9001"])
            if self.clear:
                os.system("cls")
        else:
            sys.stdout.write(f"\033[8;{self.restore_lines};"
                             f"{self.restore_columns}t")
            sys.stdout.flush()
            if self.clear:
                os.system("clear")
        return False
