from typing import Any, Dict, List, Union

import requests

from src.main.api.requests.requester import Requester


class GetTransactionsRequester(Requester):

    def post(self, model):  
        raise NotImplementedError("GetTransactionsRequester only supports GET requests")

    def get(self, account_id: int) -> Union[List[Dict[str, Any]], Dict[str, Any], str]:
        url = f"{self.base_url}/accounts/{account_id}/transactions"
        response = requests.get(url=url, headers=self.headers)
        self.response_spec(response)

        if not response.headers.get("Content-Type", "").startswith("application/json"):
            return response.text

        data = response.json()
        return data
