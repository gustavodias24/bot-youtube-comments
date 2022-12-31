import sys
import time


class Loader:
    def __init__(self):
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]

    def animated_loading(self):
        for step in self.steps:
            sys.stdout.write('\r' + 'Executando...' + step)
            time.sleep(.1)
            sys.stdout.flush()
