
import pytest
import requests

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.requests.admin_user_requester import AdminUserRequester

from src.main.api.generators.random_data import RandomData
from src.main.constants.roles import Roles


class TestCreateAccount:

    @pytest.mark.acc
    @pytest.mark.parametrize("username, password, role",
        [(RandomData.get_username(), RandomData.get_password( ), Roles.USER)])
    def test_create_account(self, username, password, role):
        create_user_request = CreateUserRequest(username=username, password=password, role=role)
        create_user_response = AdminUserRequester(
            RequestSpec.admin_auth_spec(),
            ResponseSpec.entity_was_created()
        ).post(create_user_request)

        assert create_user_response.username == create_user_request.username
        assert create_user_response.role == create_user_request.role

        create_account_response = CreateAccountRequester(
            RequestSpec.user_auth_spec(create_user_request.username, create_user_request.password),
            ResponseSpec.entity_was_created()
        ).post()

        assert create_account_response.balance == 0.0
        assert not create_account_response.transactions
