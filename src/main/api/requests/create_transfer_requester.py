from typing import Any, Dict, Union

import requests

from src.main.api.models.create_transfer import CreateTransferRequest
from src.main.api.requests.requester import Requester


class CreateTransferRequester(Requester):
    def post(self, create_transfer_request: CreateTransferRequest) -> Union[Dict[str, Any], str]:
        url = f"{self.base_url}/accounts/transfer"
        response = requests.post(
            url=url,
            json=create_transfer_request.model_dump(),
            headers=self.headers,
        )
        self.response_spec(response)

        if not response.headers.get("Content-Type", "").startswith("application/json"):
            return response.text

        return response.json()
