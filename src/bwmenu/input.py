import subprocess
from os import getenv

def qute_command(command:str):
    """Launch a qutebrowser command"""
    fifo = getenv('QUTE_FIFO')
    assert fifo is not None
    with open(fifo, 'w') as fifo:
        fifo.write(command + '\n')
        fifo.flush()

def xdotool(*args:str):
    """xdotool wrapper"""
    cmd = ["xdotool"] + list(args)
    subprocess.check_output(cmd)

def type_word(word: str, qute: bool = False):
    if qute:
        qute_command(f"insert-text {word}")
    else:
        xdotool("type", word)

def type_tab(qute: bool = False):
    """simulate pressing the tab key"""
    if qute:
        qute_command(f"fake-key <Tab>")
    else:
        xdotool("key", "Tab")

def type_return(qute: bool = False):
    """simulate pressing the return key"""
    if qute:
        qute_command(f"fake-key <Enter>")
    else:
        xdotool("key", "Return")
