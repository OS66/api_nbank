from http import HTTPStatus
import requests

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse

from src.main.api.requests.requester import Requester




class AdminUserRequester(Requester):
    def post(self, create_user_request: CreateUserRequest) -> CreateUserResponse:
        url = f'{self.base_url}/admin/users'
        response = requests.post(url=url,json=create_user_request.model_dump(),headers=self.headers)
        self.response_spec(response)
        if  response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            return CreateUserResponse(**response.json())
        return  

    def delete(self, id: int):
        url = f"{self.base_url}/admin/users/{id}"
        response = requests.delete(url=url, headers=self.headers)
        self.response_spec(response)
        return response    