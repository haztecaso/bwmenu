from typing import List

from .utils import process_run, ProcessError
from .bin import bw
from .rofi import ask_password
from .item import Item, parse_item_list, encode_item_list
from .gpg import Cache


SESSION_CACHE_FILE = "/tmp/bw_session_cache.gpg"
LIST_CACHE_FILE = "/tmp/bw_list_cache.gpg"


class BitWarden():
    """
    Class that wraps and reimplements some funcrionality of bitwarden-cli.
    Also uses the gpg wrappers defined in .gpg to cache the data into files for
    faster loading of credentials
    """

    def __init__(self):
        self._session_key = None
        self._item_list = None
        self.session_cache = Cache(SESSION_CACHE_FILE)
        self.list_cache = Cache(LIST_CACHE_FILE)

    def clear_cache(self, **kwargs):
        if kwargs.get("--clear-cache"):
            self.list_cache.clear()
            return True
        elif kwargs.get("--clear-all-cache"):
            self.session_cache.clear()
            self.list_cache.clear()
            return True
        else:
            return False

    @property
    def session_key(self):
        """
        bitwarden-cli session key.
        If self._session_key is None the key will be fetched from the cache or
        from an interactive rofi menu and then stored into self._session_key
        """
        if not self._session_key:
            self.set_session_key_from_cache()
        if not self._session_key:
            self.set_session_key_interactive()
        return self._session_key

    def set_session_key_interactive(self):
        """
        Interactively asks the user for the master password and if it's valid
        gets the session key and stores it into self._session_key
        """
        master_password = ask_password("Master Password")
        if len(master_password) > 0:
            try:
                cmd = [bw, 'unlock', '--raw', master_password]
                self._session_key, _, _ = process_run(cmd)
            except ProcessError:
                raise AuthError("Invalid master password")
            else:
                self.session_cache.save(self._session_key)
        else:
            raise AuthError("You must enter a non-empty master password")

    def set_session_key_from_cache(self):
        """
        Tries to get the session key from the cache file and set the
        self._session_key property
        """
        self.session_cache.load_silent()
        self._session_key = self.session_cache.data

    def _run_subcmd(self, subcmd: List[str]):
        """
        Runs a bitwarden-cli sub command with the --session parameter set to the
        self.session_key
        """
        cmd = [bw] + subcmd + ["--session", self.session_key]
        stdout, _, _ = process_run(cmd)
        return stdout

    def lock(self):
        """
        Locks the bitwarden-cli session and deletes the session key from memory
        and cache files. Also deletes the item list cache
        """
        self._session_key = None
        self.session_cache.clear()
        self.list_cache.clear()
        process_run([bw, "lock"])

    @property
    def item_list(self):
        """
        Item list.
        If self._item_list is None the list will be fetched from the cache or
        from bitwarden-cli and then stored into self._item_list
        """
        if not self._item_list:
            self.set_item_list_from_cache()
        if not self._item_list:
            self.set_item_list_from_bw()
        return self._item_list

    def set_item_list_from_bw(self):
        """Runs bitwarden-cli to fetch the item list"""
        subcmd = ["list", "items"]
        try:
            self._item_list = parse_item_list(self._run_subcmd(subcmd))
        except ProcessError:
            raise AuthError("Invalid session key")
        else:
            encoded_item_list = encode_item_list(self._item_list)
            self.list_cache.save(encoded_item_list)

    def set_item_list_from_cache(self):
        """
        Tries to get the item list from the cache file and set the
        self._item_list property
        """
        self.list_cache.load_silent(parse_item_list)
        self._item_list = self.list_cache.data

    def search_item_by_url(self, url:str, bw_mode:bool = False) -> List[Item]:
        """
        Search items by url.

        Parameters
        ----------
        url: url search parameter.
        bw_mode: wether to use bitwarden-cli's own matching functionality or the
        custom matching algorithm.
        """
        if bw_mode:
            result = self.search_item_by_url_bw(url)
        else:
            result = self.search_item_by_url_custom(url)
        return result

    def search_item_by_url_custom(self, url:str) -> List[Item]:
        """
        Search an item by using the custom matching algorithm.
        The matching algorithm is implemented in the match_url method of the
        Item class.
        """
        # TODO: optimize
        return [item for item in self.item_list if item.match_url(url)]

    def search_item_by_url_bw(self, url:str) -> List[Item]:
        """Search an item by url using bitwarden-cli"""
        subcmd = ["list", "items", "--url", url]
        try:
            return parse_item_list(self._run_subcmd(subcmd))
        except ProcessError:
            raise AuthError("Invalid session key")


class AuthError(Exception):
    """Custom error for handling authentication errors"""

    def __init__(self, reason):
        self.reason = reason
        super().__init__(self.reason)

