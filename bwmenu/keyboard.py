import subprocess

from .bin import xdotool

def run(*args:str):
    subprocess.run((xdotool, ) + args)

def type_word(word: str):
    run("type", word)

def type_tab():
    run("key", "Tab")

def type_return():
    run("key", "Return")
