"""
Usage:
  bwmenu [options]

Options:
  -h, --help
      Show this help text and exit.
  -v, --version
      Show version information and exit.
  -u, --url URL
      Filter items that match this url basename.
  --bw-match
      Use bitwarden-cli to match urls instead of custom implementation.
  -c, --clear-cache
      Clear item list cache file.
  -C, --clear-all-cache
      Clear item list and session key cache files.
"""

from docopt import docopt
from os import getenv

from .utils import ProcessError
from .bitwarden import BitWarden, AuthError
from .rofi import select_item, error_message


def run(args, bw, qute, url):
    if url:
        items = bw.search_item_by_url(url, args['--bw-match'])
    else:
        items = bw.item_list
    if len(items) == 0:
        error_message("No items found")
    else:
        try: item = select_item(items)
        except ProcessError: print("Item not selected...")
        else: item.type_all(qute=qute)


def main():
    args = docopt(__doc__, version="bitwarden v0.1.1")
    bw = BitWarden()
    qute = getenv("QUTE_MODE") == "command"
    url = getenv("QUTE_URL") if qute else args.get("--url")
    if not bw.clear_cache(**args) or url:
        try:
            run(args, bw, qute, url)
        except AuthError as e:
            error_message(f'AuthError: {e.reason}')


if __name__ == "__main__":
    main()
