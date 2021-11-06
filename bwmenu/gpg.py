import os

from .utils import process_run, ProcessError
from .bin import gpg


def encrypt(path: str, data: str):
    """gpg wrapper for encrypting strings and saving them into files"""
    cmd = [gpg, "-e", "--default-recipient-self", "--armor"]
    stdout, _, _ = process_run(cmd, data)
    with open(path, "w") as f:
        f.write(stdout)


def decrypt(path: str) -> str:
    """gpg wrapper for decrypting files"""
    cmd = [gpg, "-qd", "--default-recipient-self", path]
    stdout, stderr, error_code = process_run(cmd, ignore_error=True)
    if error_code != 0:
        raise DecryptionError(stderr)
    return stdout


class DecryptionError(Exception):
    """Custom error for handling decryption errors"""
    pass


class Cache():
    """Custom class for encrypted caching"""

    def __init__(self, path, data = None):
        self.path = path
        self.data = data
        self.error = False

    def save(self, new_data = None):
        """Store the data (or new data) into the encrypted file"""
        if new_data:
            self.data = new_data
        encrypt(self.path, str(self.data))

    def load(self, decode_fn = (lambda x : x)):
        """
        Load the data from the encrypted file

        Parameters
        ----------
        decode_fn: function
          Function that parses the raw data string into the desired type
        """
        try:
            raw_data = decrypt(self.path)
            self.data = decode_fn(raw_data)
            self.error = False
        except DecryptionError:
            self.data = None
            self.error = True
        return self.data

    def load_silent(self, *args):
        """Like self.load but ignoring ProcessError's"""
        try:
            self.load(*args)
        except ProcessError:
            pass

    def clear(self):
        """Delete the cache file"""
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass

