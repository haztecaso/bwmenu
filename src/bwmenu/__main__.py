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
  -c, --clear-session
      Clear session cache.
"""

from docopt import docopt
from os import getenv

from input import type_tab, type_word

from .rofi import select_item

from .client import Client


def main():
    args = docopt(__doc__, version="bwmenu v0.2.0")
    cli = Client()
    if args["--clear-session"]:
        del cli.session.value
    if cli.session.value is None:
        cli.unlock_interactive()
    qute = getenv("QUTE_MODE") == "command"
    if qute:
        baseurl = getenv("QUTE_URL")
        assert baseurl is not None
    else:
        baseurl = args["--url"]
        baseurl = "" if baseurl is None else baseurl
    item = select_item(cli.items_by_url(baseurl))
    if item.login.username is not None:
        type_word(item.login.username, qute)
    if item.login.username is not None and item.login.password is not None:
        type_tab(qute)
    if item.login.password is not None:
        type_word(item.login.password, qute)

if __name__ == "__main__":
    main()
