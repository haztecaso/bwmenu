from .bin import xdotool
from .utils import process_run


def run(*args:str):
    process_run([xdotool] + list(args))

def type_word(word: str):
    run("type", word)

def type_tab():
    run("key", "Tab")

def type_return():
    run("key", "Return")
