import subprocess

from .utils import process_run
from .bin import gpg

def encrypt(path: str, data: str):
    cmd = [gpg, "-e", "--default-recipient-self", "--armor"]
    stdout, _ = process_run(cmd, data)
    with open(path, "w") as f:
        f.write(stdout)

def decrypt(path: str) -> str:
    cmd = [gpg, "-qd", "--default-recipient-self", path]
    stdout, _ = process_run(cmd)
    return stdout
