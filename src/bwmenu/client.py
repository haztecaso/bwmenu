from functools import cached_property
import json
import subprocess

from .rofi import rofi_password

from .item import Item, Login, Uri

from .cachedstr import CachedStr

SESSION_CACHE_FILE = "/tmp/bwmenu_session"


class Client:
    def __init__(self):
        self.session: CachedStr = CachedStr(SESSION_CACHE_FILE)

    def unlock(self, password: str) -> bool:
        try:
            session = subprocess.check_output(
                ["bw", "unlock", "--raw", password], stderr=subprocess.DEVNULL
            )
            self.session.value = session.decode()
            return True
        except subprocess.CalledProcessError:
            return False

    def unlock_interactive(self, attempts: int = 3) -> bool:
        password = rofi_password("Bitwarden master password")
        if self.unlock(password[0:-1]):
            return True
        elif attempts > 1:
            return self.unlock_interactive(attempts-1)
        else:
            return False


    @property
    def _session_param(self):
        if self.session.value is not None:
            return ["--session", self.session.value]
        else:
            return []

    @cached_property
    def items(self) -> list[Item]:
        data = json.loads(
            subprocess.check_output(["bw", "list", "items"] + self._session_param)
        )
        assert isinstance(data, list)
        items :list[Item]= []
        for obj in data:
            if "id" in obj and "name" in obj and "login" in obj:
                uris = []
                if "uris" in obj["login"]:
                    for raw_uri in obj["login"]["uris"]:
                        uris.append(Uri(**raw_uri))
                obj["login"]["uris"] = uris
                login = Login(**obj["login"])
                items.append(Item(id=obj["id"], name=obj["name"], login=login))
        return items

    def items_by_url(self, baseurl:str):
        return [item for item in self.items if item.match(baseurl)]

