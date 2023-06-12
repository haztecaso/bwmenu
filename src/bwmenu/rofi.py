from typing import List

from .utils import process_run
from .item import Item


def rofi(title:str, extra_options:List[str], stdin:str="") -> str:
    """rofi wrapper"""
    cmd = ["rofi", "-dmenu", "-p", title] + extra_options
    stdout, _, _ = process_run(cmd, stdin)
    return stdout


def error_message(message:str):
    """display a message with rofi"""
    return process_run(["rofi", "-e", message + "!"])


def ask_password(title: str) -> str:
    """prompt the user for a password"""
    return rofi(title, ["-password", "-lines", "0"])


def select_item(items:List[Item]):
    """Select item from an item list"""
    if len(items) == 1: return items[0]
    id = rofi("Item", [],
                '\n'.join([str(item) for item in items])
            ).split("[id: ")[1][0:-1]
    for item in items:
        if item.id == id:
            return item
