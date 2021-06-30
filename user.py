from helper import Helper, UnauthorizedError
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
import json


class User(Helper):
    '''
        The User base class provides all user APIs like listing users, metadata like media, rooms, creating, modifying users.
    '''

    def __init__(self, access_token: str, homeserver_url: str) -> None:
        super().__init__(access_token, homeserver_url)

    def list_all(self):
        '''
            List all users registered in the server.
        '''
        req = Request(urljoin(self.homeserver_url, "/_synapse/admin/v2/users?from=0&limit=10&guests=false"),
                      headers={"Authorization": "Bearer {}".format(self.access_token)})
        response = {}
        try:
            response = json.loads(urlopen(req).read().decode())
        except HTTPError as e:
            if e.code == 401:
                raise UnauthorizedError
        return response

    def get_user(self, user_id):
        '''
            Get details for a user.
                user_id: required, Provide user_id as '@username:domain.tld'
        '''
        req = Request(urljoin(self.homeserver_url, "/_synapse/admin/v2/users/{}".format(user_id)),
                      headers={"Authorization": "Bearer {}".format(self.access_token)})
        response = {}
        try:
            response = json.loads(urlopen(req).read().decode())
        except HTTPError as e:
            if e.code == 401:
                raise UnauthorizedError
        return response

    def get_sessions(self, user_id):
        req = Request(urljoin(self.homeserver_url, "/_synapse/admin/v1/whois/{}".format(user_id)),
                      headers={"Authorization": "Bearer {}".format(self.access_token)})
        response = {}
        try:
            response = json.loads(urlopen(req).read().decode())
        except HTTPError as e:
            if e.code == 401:
                raise UnauthorizedError
        return response

    def is_admin(self, user_id):
        req = Request(urljoin(self.homeserver_url, "/_synapse/admin/v1/users/{}/admin".format(user_id)),
                      headers={"Authorization": "Bearer {}".format(self.access_token)})
        response = {}
        try:
            response = json.loads(urlopen(req).read().decode())
        except HTTPError as e:
            if e.code == 401:
                raise UnauthorizedError
        return response

    def get_room_memberships(self, user_id):
        '''
            List all the rooms a user is in currently.
                user_id: required, Provide user ID as '@username:domain.tld'\n
        '''
        req = Request(urljoin(self.homeserver_url, "/_synapse/admin/v1/users/{}/joined_rooms".format(user_id)),
                      headers={"Authorization": "Bearer {}".format(self.access_token)})
        response = {}
        try:
            response = json.loads(urlopen(req).read().decode())
        except HTTPError as e:
            if e.code == 401:
                raise UnauthorizedError
        return response

    def list_media(self, user_id):
        req = Request(urljoin(self.homeserver_url, "/_synapse/admin/v1/users/{}/media".format(user_id)),
                      headers={"Authorization": "Bearer {}".format(self.access_token)})
        response = {}
        try:
            response = json.loads(urlopen(req).read().decode())
        except HTTPError as e:
            if e.code == 401:
                raise UnauthorizedError
        return response

    def create_user(self, user_id: str, password: str, displayname: str = None, is_admin: bool = False, is_deactivated: bool = False):
        if displayname is None:
            displayname = user_id
        body = {
            "password": password,
            "displayname": displayname,
            "admin": is_admin,
            "deactivated": is_deactivated
        }
        req = Request(urljoin(self.homeserver_url, "/_synapse/admin/v2/users/{}".format(user_id)),
                      headers={"Authorization": "Bearer {}".format(self.access_token)}, method='PUT', data=json.dumps(body).encode())
        response = {}
        try:
            response = json.loads(urlopen(req).read().decode())
        except HTTPError as e:
            if e.code == 401:
                raise UnauthorizedError
        return response

    def edit_user(self, user_id: str, password: str = None, displayname: str = None,
                  is_admin: bool = False, is_deactivated: bool = False, threepids: list = [], avatar_url: str = None):

        body = {
            "password": "",
            "displayname": "",
            "threepids": [],
            "avatar_url": "",
            "admin": False,
            "deactivated": False
        }

        if displayname is None:
            del body["displayname"]
        if password is None:
            del body["password"]
        if len(threepids) == 0:
            del body["threepids"]
        if avatar_url is None:
            del body["avatar_url"]
        if is_admin:
            body["admin"] = True
        if is_deactivated:
            body["deactivated"] = True

        req = Request(urljoin(self.homeserver_url, "/_synapse/admin/v2/users/{}".format(user_id)),
                      headers={"Authorization": "Bearer {}".format(self.access_token)}, method='PUT', data=json.dumps(body).encode())
        response = {}
        try:
            response = json.loads(urlopen(req).read().decode())
        except HTTPError as e:
            if e.code == 401:
                raise UnauthorizedError
        return response

    def deactivate_user(self, user_id: str, erase: bool = False):
        body = {}
        if erase:
            body = {
                "erase": True
            }
        req = Request(urljoin(self.homeserver_url, "/_synapse/admin/v1/deactivate/{}".format(user_id)),
                      headers={"Authorization": "Bearer {}".format(self.access_token)}, data=json.dumps(body).encode())
        response = {}
        try:
            response = json.loads(urlopen(req).read().decode())
        except HTTPError as e:
            if e.code == 401:
                raise UnauthorizedError
        return response

    def reset_password(self, user_id: str, new_password: str, logout_devices: bool = True):
        '''
            Change a user's password.\n
                user_id: required, Provide user ID as '@username:domain.tld'\n
                new_password: required\n
                logout_devices: optional, default is True
        '''
        body = {
            "new_password": new_password,
            "logout_devices": True
        }

        if not logout_devices:
            body["logout_devices"] = False

        req = Request(urljoin(self.homeserver_url, "/_synapse/admin/v1/reset_password/{}".format(user_id)),
                      headers={"Authorization": "Bearer {}".format(self.access_token)}, data=json.dumps(body).encode())
        response = {}
        try:
            response = json.loads(urlopen(req).read().decode())
        except HTTPError as e:
            if e.code == 401:
                raise UnauthorizedError
        return response

    def is_admin(self, user_id: str):
        '''
            Check whether a user is a server administrator or not.
                user_id: required, Provide user ID as '@username:domain.tld'\n
        '''
        req = Request(urljoin(self.homeserver_url, "/_synapse/admin/v1/users/{}/admin".format(user_id)),
                      headers={"Authorization": "Bearer {}".format(self.access_token)})
        response = {}
        try:
            response = json.loads(urlopen(req).read().decode())
        except HTTPError as e:
            if e.code == 401:
                raise UnauthorizedError
        return response
