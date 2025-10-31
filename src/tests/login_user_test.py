import pytest
import requests

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.generators.random_data import RandomData



@pytest.mark.logins
class TestLoginUser:
    @pytest.mark.login
    @pytest.mark.parametrize(
        "username, password, role",
        [(
            RandomData.get_username(),RandomData.get_password(),"USER"
        )])
    def test_login_user(self, username:str, password:str, role:str):
        create_user_request = CreateUserRequest(username=username, password=password, role=role)
        create_user_response = AdminUserRequester(
            RequestSpec.admin_auth_spec(),
            ResponseSpec.entity_was_created()
        ).post(create_user_request)

        assert create_user_response.username == create_user_request.username
        assert create_user_response.role == create_user_request.role

        login_user_request= LoginUserRequest(username=username, password=password)
        login_user_response= LoginUserRequester(
            RequestSpec.unauth_spec(),
            ResponseSpec.request_return_ok()
            ).post(login_user_request)
    
        assert login_user_request.username == login_user_response.username 
      
 

    @pytest.mark.admin
    def test_admin_login(self):
        login_admin_request = LoginUserRequest(username="admin", password="admin")

        login_admin_response= LoginUserRequester(
            RequestSpec.unauth_spec(),
            ResponseSpec.request_return_ok()
            ).post(login_admin_request)
    
        assert login_admin_response.username == login_admin_request.username
        assert login_admin_response.role =="ADMIN"