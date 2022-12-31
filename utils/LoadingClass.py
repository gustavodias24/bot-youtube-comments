import sys
import time
from colorama import Style, Fore


class Loader:
    def __init__(self, text):
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.text = text

    def animated_loading(self):
        for step in self.steps:
            sys.stdout.write(Style.RESET_ALL + Fore.BLUE + Style.BRIGHT + '\r' + f'{self.text}...' + step)

            time.sleep(.1)
            sys.stdout.flush()
