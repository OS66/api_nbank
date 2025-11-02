from typing import Any, Dict, Union

import requests

from src.main.api.requests.requester import Requester
from src.main.api.models.get_profile_response import GetProfileResponse



class GetProfileRequester(Requester):
    def get(self):
        url = f'{self.base_url}/customer/profile'
        response = requests.get(url=url, headers=self.headers)
        self.response_spec(response)
        return GetProfileResponse(**response.json()) 

    def post(self):
        pass


