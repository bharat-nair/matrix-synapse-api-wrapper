from urllib.request import Request, urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
import json


class UnauthorizedError(Exception):
    def __init__(self, message="Invalid Access Token") -> None:
        self.message = message
        super().__init__(self.message)


class Helper():
    def __init__(self, access_token: str, homeserver_url: str) -> None:
        self.access_token = access_token
        self.homeserver_url = homeserver_url
