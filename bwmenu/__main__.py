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

from .bitwarden import BitWarden
from .rofi import select_item, error_message

def main():
    args = docopt(__doc__, version="bitwarden v0.0.1")
    bw = BitWarden()
    qutebrowser = getenv("QUTE_MODE") == "command"
    items = bw.list_items_by_url(getenv("QUTE_URL")) if qutebrowser\
            else bw.list_items()
    if len(items) == 0:
        error_message("No items found")
        return
    item = items[0] if len(items) == 1 else select_item(items)
    print(item)


if __name__ == "__main__":
    main()
