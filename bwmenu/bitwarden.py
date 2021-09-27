from typing import List

from .utils import process_run, ProcessError
from .bin import bw
from .rofi import ask_password
from .item import Item, parse_item_list, encode_item_list
from .gpg import Cache


SESSION_CACHE_FILE = "/tmp/bw_session_cache.gpg"
LIST_CACHE_FILE = "/tmp/bw_list_cache.gpg"


class BitWarden():

    def __init__(self):
        self._session_key = None
        self._item_list = None
        self.session_cache = Cache(SESSION_CACHE_FILE)
        self.list_cache = Cache(LIST_CACHE_FILE)

    @property
    def session_key(self):
        if not self._session_key:
            self.session_cache.load_silent()
            self._session_key = self.session_cache.data
            if not self._session_key:
                master_password = ask_password("Master Password")
                try:
                    self._session_key = self.get_session_key(master_password)
                    self.session_cache.save(self._session_key)
                except ProcessError:
                    raise AuthError("Invalid master password")
        return self._session_key

    def get_session_key(self, master_password: str) -> str:
        if len(master_password) > 0:
            stdout, _, _ = process_run([bw, 'unlock', '--raw', master_password])
        else:
            raise AuthError("You must enter a non-empty master password")
        return stdout

    def run_subcmd(self, subcmd: List[str]):
        cmd = [bw] + subcmd + ["--session", self.session_key]
        stdout, _, _ = process_run(cmd)
        return stdout

    def lock(self):
        self._session_key = None
        process_run([bw, "lock"])

    @property
    def item_list(self):
        if not self._item_list:
            self.list_cache.load_silent(parse_item_list)
            self._item_list = self.list_cache.data
            if not self._item_list:
                self._item_list = self.get_item_list()
                encoded_item_list = encode_item_list(self._item_list)
                self.list_cache.save(encoded_item_list)
        return self._item_list

    def get_item_list(self) -> List[Item]:
        subcmd = ["list", "items"]
        try:
            return parse_item_list(self.run_subcmd(subcmd))
        except ProcessError:
            raise AuthError("Invalid session key")

    def search_item_by_url(self, url:str, bw_mode = False) -> List[Item]:
        if bw_mode:
            result = self.search_item_by_url_bw(url)
        else:
            result = self.search_item_by_url_custom(url)
        return result

    def search_item_by_url_custom(self, url:str) -> List[Item]:
        return [item for item in self.item_list if item.match_url(url)]

    def search_item_by_url_bw(self, url:str) -> List[Item]:
        subcmd = ["list", "items", "--url", url]
        try:
            return parse_item_list(self.run_subcmd(subcmd))
        except ProcessError:
            raise AuthError("Invalid session key")



class AuthError(Exception):

    def __init__(self, reason):
        self.reason = reason
        super().__init__(self.reason)


def match_detect_basename(uris, current_url):
    pass
