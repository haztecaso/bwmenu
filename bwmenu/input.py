from os import getenv

from .bin import xdotool as xdotool_bin
from .utils import process_run

def qute_command(command):
    with open(getenv('QUTE_FIFO'), 'w') as fifo:
        fifo.write(command + '\n')
        fifo.flush()

def xdotool(*args:str, **kwargs:bool):
    process_run([xdotool_bin] + list(args))

def type_word(word: str, **kwargs):
    if kwargs.get("qute"):
        qute_command(f"insert-text {word}")
        pass
    else:
        xdotool("type", word, **kwargs)

def type_tab(**kwargs):
    if kwargs.get("qute"):
        qute_command(f"fake-key <Tab>")
    else:
        xdotool("key", "Tab", **kwargs)

def type_return(**kwargs):
    if kwargs.get("qute"):
        qute_command(f"fake-key <Enter>")
    else:
        xdotool("key", "Return", **kwargs)
