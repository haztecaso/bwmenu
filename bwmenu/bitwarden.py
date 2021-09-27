from typing import List

from .utils import process_run, ProcessError
from .rofi import ask_password
from .item import Item, parse_item_list
from .bin import bw


class BitWarden():
    def __init__(self):
        self._session_key = None
        self._session_key = "yn8WWarH2PaC/Pd8umsTeFj4ORLS8VbVjWYVQubDaBHA+2XjQOq0BakRsfgO8mxJ2LnLsYSeBRVCTUWuKVMV9Q=="

    def get_session_key(self, master_password: str) -> str:
        if len(master_password) > 0:
            stdout, _= process_run([bw, 'unlock', '--raw', master_password])
        else:
            raise AuthError("You must enter a non-empty master password")
        return stdout

    @property
    def session_key(self) -> str:
        if self._session_key:
            result = self._session_key
        else:
            master_password = ask_password("Master Password")
            try:
                self._session_key = self.get_session_key(master_password)
            except ProcessError:
                raise AuthError("Invalid master password")
            else:
                result = str(self._session_key)
        return result

    def run_subcmd(self, subcmd: List[str]):
        cmd = [bw] + subcmd + ["--session", self.session_key]
        stdout, _ = process_run(cmd)
        return stdout

    def cache_session_key(self):
        raise NotImplementedError()

    def clear_cache_session_key(self):
        raise NotImplementedError()

    def load_cached_session_key(self):
        raise NotImplementedError()

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


