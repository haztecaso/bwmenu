"""
Usage:
  bwmenu [options]

Options:
  -h, --help
      Show this help text and exit.
  -v, --version
      Show version information and exit.
  --bw-match
      Use bitwarden-cli to match urls instead of custom implementation.
  -c, --clear-cache
      Clear cache files.
  -C, --clear-items-cache
      Only clear item list cache file.
"""

from docopt import docopt
from os import getenv

from .utils import ProcessError
from .bitwarden import BitWarden, AuthError
from .rofi import select_item, error_message

def run():
    args = docopt(__doc__, version="bitwarden v0.1.1")
    bw = BitWarden()
    if args.get("--clear-cache"):
        bw.session_cache.clear()
        bw.list_cache.clear()
    elif args.get("--clear-items-cache"):
        bw.list_cache.clear()
    qutebrowser = getenv("QUTE_MODE") == "command"
    if qutebrowser:
        items = bw.search_item_by_url(getenv("QUTE_URL"), args['--bw-match'])
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
            item.type_all(qute = qutebrowser)


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

