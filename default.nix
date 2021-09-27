{ python38Packages, lib, bitwarden-cli, gnupg, libnotify, rofi, xdotool }:

python38Packages.buildPythonPackage rec {
  pname = "bwmenu";
  version = "0.0.1";

  src = ./.;

  propagatedBuildInputs = with python38Packages; [ docopt ];

  # checkInputs = [ pkgs.python38Packages.pytest ];
  # checkPhase = "pytest";

  postInstall = ''
    substituteInPlace $out/lib/*/site-packages/bwmenu/bin.py\
      --replace "\"bw\"" "\"${bitwarden-cli}/bin/bw\""\
      --replace "\"gpg\"" "\"${gnupg}/bin/gpg\""\
      --replace "\"notify-send\"" "\"${libnotify}/bin/notify-send\""\
      --replace "\"rofi\"" "\"${rofi}/bin/rofi\""\
      --replace "\"xdotool\"" "\"${xdotool}/bin/xdotool\""
  '';

  meta = with lib; {
    homepage = "https://github.com/haztecaso/bitwarden-cli";
    description = "bitwarden-cli rofi wrapper";
    license = licenses.gpl3;
  };
}

