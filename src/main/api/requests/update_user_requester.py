from http import HTTPStatus
import requests

from src.main.api.models.update_profile_request import UpdateProfileRequest
from src.main.api.models.update_profile_response import UpdateProfileResponse
from src.main.api.requests.requester import Requester


class UpdateProfileRequester(Requester):
    def post(self, model: UpdateProfileRequest):
        raise NotImplementedError("UpdateProfileRequester supports only PUT requests")

    def put(self, payload: dict) -> UpdateProfileResponse:
        url = f"{self.base_url}/customer/profile"
        response = requests.put(
            url=url,
            json=payload,
            headers=self.headers,
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            return UpdateProfileResponse(**response.json())
        return response  
