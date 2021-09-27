import os

from .utils import process_run, ProcessError
from .bin import gpg

def encrypt(path: str, data: str):
    cmd = [gpg, "-e", "--default-recipient-self", "--armor"]
    stdout, _, _ = process_run(cmd, data)
    with open(path, "w") as f:
        f.write(stdout)


def decrypt(path: str) -> str:
    cmd = [gpg, "-qd", "--default-recipient-self", path]
    stdout, stderr, error_code = process_run(cmd, ignore_error=True)
    if error_code != 0:
        raise DecryptionError(stderr)
    return stdout


class DecryptionError(Exception):
    pass


class Cache():
    
    def __init__(self, path, data = None):
        self.path = path
        self.data = data
        self.error = False

    def save(self, new_data = None):
        if new_data:
            self.data = new_data
        encrypt(self.path, str(self.data))

    def load(self, decode_fn = (lambda x : x)):
        try:
            raw_data = decrypt(self.path)
            self.data = decode_fn(raw_data)
            self.error = False
        except DecryptionError:
            self.data = None
            self.error = True
        return self.data

    def load_silent(self, *args):
        try:
            self.load(*args)
        except ProcessError:
            pass

    def clear(self):
        os.remove(self.path)

