import pytest
import logging


from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.generators.random_data import RandomData
from src.main.constants.roles import Roles

@pytest.mark.api
class TestCreateUser:
    @pytest.mark.user
    def test_create_valid_user(self):
        create_user_request = CreateUserRequest(username=RandomData.get_username(), password=RandomData.get_password(), role= Roles.USER)
        create_user_response = AdminUserRequester(
             RequestSpec.admin_auth_spec(),
             ResponseSpec.entity_was_created()
        ).post(create_user_request)

        assert create_user_response.username == create_user_request.username
        assert create_user_response.role == create_user_request.role
        logging.info(f'User was created: {create_user_response.username}, password: {create_user_request.password} ')
       

    
    
    @pytest.mark.invalid
    @pytest.mark.parametrize(
       'username, password, role, error_key, error_value',
        [ ("", "verysTRongPassword33$", Roles.USER, "username", "Username must contain only letters, digits, dashes, underscores, and dots")
        ])
    def test_create_invalid_user(self, username, password, role, error_key, error_value):
        create_user_request = CreateUserRequest(username=username, password=password, role= role)

        AdminUserRequester(
             RequestSpec.admin_auth_spec(),
             ResponseSpec.request_return_bad_request(error_key, error_value)
        ).post(create_user_request)
