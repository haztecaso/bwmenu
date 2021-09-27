from subprocess import Popen, PIPE, STDOUT
import re
from typing import List

from .bin import rofi
from .item import Item

def run(title:str, extra_options:List[str], stdin:str="") -> str:
    process = Popen(
            [rofi, "-dmenu", "-p", title] + extra_options,
            stdout=PIPE, stdin=PIPE, stderr=STDOUT
            )
    stdout = process.communicate(input=bytes(stdin, "utf-8"))[0].strip()
    return stdout.decode("utf-8")

def error_message(message:str):
    Popen(
        [rofi, "-e", message + "!"],
        stdout=PIPE, stdin=PIPE, stderr=STDOUT
    ).communicate()


def ask_password(title: str) -> str:
    return run(title, ["-password", "-lines", "0"])

def select_item(items:List[Item]):
    id = run("Item", [],
                '\n'.join([str(item) for item in items])
            ).split("[id: ")[1][0:-1]
    for item in items:
        if item.id == id:
            return item
