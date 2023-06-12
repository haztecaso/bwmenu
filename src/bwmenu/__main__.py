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

from .rofi import select_item

from .client import Client


def main():
    args = docopt(__doc__, version="bwmenu v0.2.0")
    cli = Client()
    print(f"{cli.session.value = }")
    if cli.session.value is None:
        cli.unlock_interactive()
    # baseurl = input("Url: ")
    baseurl = "haztecaso.com"

    item = select_item(cli.items_by_url(baseurl))
    print(item.login.username, item.login.password)




if __name__ == "__main__":
    main()
