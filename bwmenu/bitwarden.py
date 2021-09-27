import os
from typing import List

from .utils import process_run, ProcessError
from .bin import bw
from .rofi import ask_password
from .item import Item, parse_item_list
from .gpg import encrypt, decrypt


SESSION_CACHE_FILE = "/tmp/bw_session_cache.gpg"
LIST_CACHE_FILE = "/tmp/bw_list_cache.gpg"


class BitWarden():
    def __init__(self):
        self._session_key = None

    def get_session_key(self, master_password: str) -> str:
        if len(master_password) > 0:
            stdout, _= process_run([bw, 'unlock', '--raw', master_password])
        else:
            raise AuthError("You must enter a non-empty master password")
        return stdout

    @property
    def session_key(self) -> str:
        if not self._session_key:
            try:
                self._session_key = self.load_cached_session_key()
            except ProcessError:
                master_password = ask_password("Master Password")
                try:
                    self._session_key = self.get_session_key(master_password)
                    self.cache_session_key()
                except ProcessError:
                    raise AuthError("Invalid master password")
        return self._session_key

    def run_subcmd(self, subcmd: List[str]):
        cmd = [bw] + subcmd + ["--session", self.session_key]
        stdout, _ = process_run(cmd)
        return stdout

    def cache_session_key(self):
        encrypt(SESSION_CACHE_FILE, self.session_key)

    def clear_cache_session_key(self):
        os.remove(SESSION_CACHE_FILE)

    def load_cached_session_key(self) -> str:
        return decrypt(SESSION_CACHE_FILE)

    def lock(self):
        self._session_key = None
        process_run([bw, "lock"])

    def list_items(self, url=None) -> List[Item]:
        subcmd = ["list", "items"]
        if url:
            subcmd += ["--url", url]
        try:
            return parse_item_list(self.run_subcmd(subcmd))
        except ProcessError:
            raise AuthError("Invalid session key")


class AuthError(Exception):

    def __init__(self, reason):
        self.reason = reason
        super().__init__(self.reason)


