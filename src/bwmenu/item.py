from pydantic import BaseModel


class Uri(BaseModel):
    uri: str | None

    def match(self, baseurl: str):
        if self.uri is None:
            return False
        return baseurl in self.uri


class Login(BaseModel):
    uris: list[Uri]
    username: str | None
    password: str | None
    totp: str | None

    def match(self, baseurl: str):
        return any([uri.match(baseurl) for uri in self.uris])


class Item(BaseModel):
    id: str
    name: str
    login: Login

    def match(self, baseurl: str):
        return self.login.match(baseurl)
