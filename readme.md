# bitwarden-rofi (bwmenu)

bitwarden-cli rofi wrapper written in python and with qutebrowser userscripts support.

## Installing

This script is intended for use with a nix or nixos system. The file
`default.nix` contains the derivation (package) declaration and `shell.nix` the
reproducible develompent environment.

In theory you can also use this script without nix, but I have never tested it.

### Dependencies

This are the script dependencies, if you want to install them by hand:

- bitwarden-cli
- gnupg
- libnotify
- rofi
- xdotool
- python modules:
  - docopt
  - tldextract
