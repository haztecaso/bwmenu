{ pkgs ? import <nixpkgs> {} }:
let
  inherit (pkgs) lib;
  bitwarden-rofi = pkgs.callPackage ./default.nix {};
in
pkgs.mkShell {
  nativeBuildInputs = (with pkgs; [
    bitwarden-rofi
    bitwarden-cli
    gnupg
    libnotify
    rofi
    xdotool 
  ]) ++ (with pkgs.python38Packages; [
    docopt
    pytest
  ]);
  shellHook = ''
    alias bwmenu="python -m bwmenu"
    alias pytest="python -m pytest"
  '';
}
