from http import HTTPStatus
import requests


from src.main.api.models.create_deposit_request import CreateDepositRequest
from src.main.api.models.create_deposit_response import CreateDepositResponse

from src.main.api.requests.requester import Requester


class CreateDepositRequester(Requester):
     def post(self, create_deposit_request: CreateDepositRequest) -> CreateDepositResponse:
        url = f'{self.base_url}/accounts/deposit'
        response = requests.post(url=url, json=create_deposit_request.model_dump(), headers=self.headers)
        self.response_spec(response)

        if not response.headers.get("Content-Type", "").startswith("application/json"):
            return response.content
        return CreateDepositResponse(**response.json())





