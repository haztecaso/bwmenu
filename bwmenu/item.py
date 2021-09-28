from dataclasses import dataclass
import json
from typing import List

from .utils import baseurl
from .input import type_word, type_tab, type_return
from time import sleep


@dataclass(init=False, eq=False)
class Item():
    """Custom class for items"""
    id: str
    name: str
    username: str
    password: str

    def __init__(self, item: object):
        self.id = item['id']
        self.name = item['name']
        self.username = item['login']['username']
        self.password = item['login']['password']
        self.baseurls = []
        for uri_data in item['login'].get('uris', []):
            self.baseurls.append(baseurl(uri_data["uri"]))

    def __eq__(self, other):
        return self.id == other.id

    def dict(self):
        """
        Encode the data into a dictionary with a shape similar to the
        bitwarden-cli output
        """
        uris = [{"uri": baseurl} for baseurl in self.baseurls]
        return {
            'type': 1,
            'id': self.id,
            'name': self.name,
            'login' : {
                'username' : self.username, 
                'password' : self.password,
                'uris': uris
                }
            }

    def match_url(self, url):
        """
        Return true if the baseurl of the given url matches any of the item
        baseurls
        """
        return any([baseurl(url) == b for b in self.baseurls]) 

    def type_username(self, **kwargs):
        """Type the username"""
        type_word(self.username, **kwargs)

    def type_password(self, **kwargs):
        """Type the password"""
        type_word(self.password, **kwargs)

    def type_all(self, ret=True, **kwargs):
        """Type the username and password and then submit them"""
        self.type_username(**kwargs)
        sleep(0.15)
        type_tab()
        sleep(0.15)
        self.type_password(**kwargs)
        sleep(0.15)
        if ret:
            type_return(**kwargs)

    def __str__(self):
        return f"{self.name}: {self.username}\t\t[id: {self.id}]"


def parse_item_list(raw_list_json:str) -> List[Item]:
    """Parse an item list encoded in json"""
    return list(map(
            lambda i: Item(i),
            filter(
                lambda i: i['type'] == 1,
                json.loads(raw_list_json)
                )
            ))

def encode_item_list(items:List[Item]) -> str:
    """Encode an item list into json"""
    return json.dumps([item.dict() for item in items])

