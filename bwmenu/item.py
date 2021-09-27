from dataclasses import dataclass
import json
from typing import List

from .keyboard import type_word, type_tab, type_return
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

    def type_username(self):
        type_word(self.username)

    def type_password(self):
        type_word(self.password)

    def type_all(self, ret=False):
        self.type_username()
        sleep(0.15)
        type_tab()
        sleep(0.15)
        self.type_password()
        sleep(0.15)
        if ret:
            type_return()

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
