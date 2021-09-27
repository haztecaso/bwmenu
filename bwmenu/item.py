from dataclasses import dataclass
import json
from typing import List

from .input import type_word, type_tab, type_return
from time import sleep


@dataclass(init=False, eq=False)
class Item():
    id: str
    name: str
    username: str
    password: str

    def __init__(self, item: object):
        self.id = item['id']
        self.name = item['name']
        self.username = item['login']['username']
        self.password = item['login']['password']

    def __eq__(self, other):
        return self.id == other.id

    def dict(self):
        return {
            'type': 1,
            'id': self.id,
            'name': self.name,
            'login' : {
                'username' : self.username, 
                'password' : self.password
                }
            }

    def type_username(self, **kwargs):
        type_word(self.username, **kwargs)

    def type_password(self, **kwargs):
        type_word(self.password, **kwargs)

    def type_all(self, ret=False, **kwargs):
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
        return list(map(
                lambda i: Item(i),
                filter(
                    lambda i: i['type'] == 1,
                    json.loads(raw_list_json)
                    )
                ))

def encode_item_list(items:List[Item]) -> str:
    return json.dumps([item.dict() for item in items])

