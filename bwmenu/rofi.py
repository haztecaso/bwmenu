from subprocess import Popen, PIPE, STDOUT
import re
from typing import List

from .utils import process_run
from .bin import rofi
from .item import Item

def run(title:str, extra_options:List[str], input:str="") -> str:
    stdin = bytes(input, "utf-8")
    stdout, _ = process_run([rofi, "-dmenu", "-p", title] + extra_options, input)
    return stdout


def error_message(message:str):
    return process_run([rofi, "-e", message + "!"])


def ask_password(title: str) -> str:
    return run(title, ["-password", "-lines", "0"])


def select_item(items:List[Item]):
    id = run("Item", [],
                '\n'.join([str(item) for item in items])
            ).split("[id: ")[1][0:-1]
    for item in items:
        if item.id == id:
            return item
