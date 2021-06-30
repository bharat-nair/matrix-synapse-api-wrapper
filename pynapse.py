from user import User
from helper import Helper


class AdminAPI(Helper):
    '''
        This class creates an instance of the entire API. Please provide:

            access_token: required, can be obtained from your Element client\n
            homeserver_url: required, usually https://matrix.domainname.tld
    '''
    def __init__(self, access_token: str, homeserver_url: str) -> None:
        super().__init__(access_token, homeserver_url)
        self.users = User(access_token, homeserver_url)
