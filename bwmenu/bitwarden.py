import subprocess, json
from typing import List

from .rofi import ask_password, error_message
from .item import Item
from .bin import bw


class BitWarden():
    def __init__(self):
        self._session_key = None
        self._session_key = "RG/5hPgxlpN00T00Rrdn0NtCcMbf2oDFhKVycz96hx13+y06pkSQVq8T4M0iYwGigL0Y2qIdvVvdzo/1VThxMg=="

    def get_session_key(self, master_password: str) -> str:
        if len(master_password) > 0:
            return subprocess.check_output(
                [bw, 'unlock', '--raw', master_password],
                universal_newlines=True,
            ).strip()
        else:
            raise ValueError("You must enter a non-empty master password")

    @property
    def session_key(self) -> str:
        if self._session_key:
            return self._session_key
        else:
            master_password = ask_password("Master Password")
            try:
                self._session_key = self.get_session_key(master_password)
            except ValueError as e:
                error_message(str(e))
            except subprocess.CalledProcessError as e:
                error_message("Invalid master password")
            return str(self._session_key)

    def run_subcmd(self, subcmd: List[str]):
        return subprocess.check_output(
            [bw] + subcmd + ["--session", self.session_key]
        ).strip().decode("utf-8")

    def cache_session_key(self):
        raise NotImplementedError()

    def load_cached_session_key(self):
        raise NotImplementedError()

    def lock(self):
        self._session_key = None
        subprocess.run([bw, "lock"])

    def list_items(self) -> List[Item]:
        return parse_item_list(self.run_subcmd(["list", "items"]))

    def list_items_by_url(self, url:str) -> List[Item]:
        return parse_item_list(self.run_subcmd(["list", "items", "--url", url]))


def parse_item_list(raw_list_json:str) -> List[Item]:
        return list(map(
                lambda i: Item(i),
                filter(
                    lambda i: i['type'] == 1,
                    json.loads(raw_list_json)
                    )
                ))
