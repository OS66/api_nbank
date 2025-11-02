from typing import Any, Dict, Union

import requests

from src.main.api.requests.requester import Requester
from src.main.api.models.get_accounts import GetAccounts
from src.main.api.models.get_accounts_response import GetAccountsResponse



class GetAccountsRequester(Requester):
    def get(self):
        url = f'{self.base_url}/customer/accounts'
        response = requests.get(url=url, headers=self.headers)
        self.response_spec(response)
        return GetAccountsResponse(accounts=response.json())


   
