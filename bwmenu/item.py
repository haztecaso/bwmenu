from dataclasses import dataclass

from .keyboard import type_word, type_tab
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

    def type_all(self):
        self.type_username()
        sleep(0.15)
        type_tab()
        sleep(0.15)
        self.type_password()

    def __str__(self):
        return f"{self.name}: {self.username}\t\t[id: {self.id}]"
