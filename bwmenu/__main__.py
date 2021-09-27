"""
Usage:
  bwmenu [options]

Options:
  -h, --help
      Show this help text and exit.
  -v, --version
      Show version information and exit.
"""

from docopt import docopt
from os import getenv

from .utils import ProcessError
from .bitwarden import BitWarden, AuthError
from .rofi import select_item, error_message

def run():
    args = docopt(__doc__, version="bitwarden v0.0.1")
    bw = BitWarden()
    qutebrowser = getenv("QUTE_MODE") == "command"
    if qutebrowser:
        items = bw.get_item_list(getenv("QUTE_URL"))
    else:
        items = bw.item_list
    if len(items) == 0:
        error_message("No items found")
    else:
        try:
            item = items[0] if len(items) == 1 else select_item(items)
        except ProcessError:
            print("Item not selected...")
        else:
            item.type_all(True, qute = qutebrowser)


def main_loop_catch_errors(n_retries:int):
    if n_retries > 0:
        try:
            run()
        except AuthError as e:
            error_message(f'AuthError: {e.reason}')
            n_retries -= 1
            main_loop_catch_errors(n_retries)

def main():
    main_loop_catch_errors(2)

if __name__ == "__main__":
    main()

