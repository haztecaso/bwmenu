import os


class CachedStr:
    def __init__(self, path: str | os.PathLike[str]):
        self.path = path
        self._value: str | None = None

    @property
    def value(self):
        if self._value is None and os.path.isfile(self.path):
            with open(self.path, "r") as f:
                self._value = f.read()
        return self._value

    @value.setter
    def value(self, value: str):
        with open(self.path, "w") as f:
            f.write(value)
        self._value = value

    @value.deleter
    def value(self):
        self._value = None
        if os.path.isfile(self.path):
            os.remove(self.path)
