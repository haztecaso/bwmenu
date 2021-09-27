import os

from .utils import process_run, ProcessError
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


class Cache():
    
    def __init__(self, path, data = None):
        self.path = path
        self.data = data

    def save(self, new_data = None):
        if new_data:
            self.data = new_data
        encrypt(self.path, str(self.data))

    def load(self, decode_fn = (lambda x : x)):
        raw_data = decrypt(self.path)
        self.data = decode_fn(raw_data)
        return self.data

    def load_silent(self, *args):
        try:
            self.load(*args)
        except ProcessError:
            pass

    def clear(self):
        os.remove(self.path)

