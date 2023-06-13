from subprocess import Popen, PIPE

from .item import Item

def rofi(title: str, extra_options: list[str], stdin: str = "") -> str:
    """rofi wrapper"""
    cmd = ["rofi", "-dmenu", "-p", title] + extra_options
    try:
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, _ = p.communicate(stdin.encode())
        return stdout.decode()
    except Exception as e:
        raise e

def rofi_password(title: str) -> str:
    """prompt the user for a password"""
    return rofi(title, ["-password", "-theme-str", "listview { enabled: false;}"])

def select_item(items: list[Item]) -> Item:
    if len(items) == 1:
        return items[0]
    stdin = "\n".join([f"{item.name} ({item.id.split('-')[0]})" for item in items])
    answer= rofi("Item", [], stdin)
    id = answer.split(" ")[-1][1:-2]
    name = " ".join(answer.split(" ")[0:-1])
    return next(filter(lambda it: it.id.split('-')[0] == id and it.name == name, items))



