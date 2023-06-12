from os import getenv

from .utils import process_run

def qute_command(command):
    """Launch a qutebrowser command"""
    with open(getenv('QUTE_FIFO'), 'w') as fifo:
        fifo.write(command + '\n')
        fifo.flush()

def xdotool(*args:str):
    """xdotool wrapper"""
    process_run(["xdotool"] + list(args))

def type_word(word: str, **kwargs):
    """type a word"""
    if kwargs.get("qute"):
        qute_command(f"insert-text {word}")
        pass
    else:
        xdotool("type", word, **kwargs)

def type_tab(**kwargs):
    """simulate pressing the tab key"""
    if kwargs.get("qute"):
        qute_command(f"fake-key <Tab>")
    else:
        xdotool("key", "Tab", **kwargs)

def type_return(**kwargs):
    """simulate pressing the return key"""
    if kwargs.get("qute"):
        qute_command(f"fake-key <Enter>")
    else:
        xdotool("key", "Return", **kwargs)
