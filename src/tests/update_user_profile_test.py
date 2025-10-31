from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.update_profile_response import UpdateProfileResponse
from src.main.api.models.update_profile_request import UpdateProfileRequest
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.requests.update_user_requester import UpdateProfileRequester

import pytest
import logging


class TestUpdateProfile():
   
    @pytest.mark.parametrize(
        "username, password, role, name",
        [(RandomData.get_username(), RandomData.get_password(),
          "USER", RandomData.get_name())],
    )
    def test_update_profile_name(self, username, password, role, name):
        create_user_request = CreateUserRequest(
            username=username, password=password, role=role)
        create_user_response = AdminUserRequester(
            RequestSpec.admin_auth_spec(),
            ResponseSpec.entity_was_created()
        ).post(create_user_request)

        assert create_user_response.username == create_user_request.username

        login_user_request = LoginUserRequest(
            username=username, password=password)
        login_user_response = LoginUserRequester(
            RequestSpec.unauth_spec(),
            ResponseSpec.request_return_ok()
            ).post(login_user_request)

        assert login_user_request.username == login_user_response.username

        update_profile_payload = UpdateProfileRequest(name=name)
        update_profile_response = UpdateProfileRequester(
            RequestSpec.user_auth_spec(username, password),
            ResponseSpec.request_return_ok(),
        ).put(update_profile_payload.model_dump())

        assert update_profile_response.customer.get(
            "name") == update_profile_payload.name
        logging.info(
            f'Old name "{login_user_request.username}" and new name "{update_profile_payload.name}"')


    @pytest.mark.test
    @pytest.mark.parametrize(
        "name, password, role,username, error_key, error_value",
        [("John", RandomData.get_password(), "USER", RandomData.get_name(),"username","Username must contain only letters, digits, dashes, underscores, and dots"),
          ("John   Smith", RandomData.get_password(), "USER", RandomData.get_name(),"username","Username must contain only letters, digits, dashes, underscores, and dots"),
          ("John123 Smith", RandomData.get_password(), "USER", RandomData.get_name(),"username","Username must contain only letters, digits, dashes, underscores, and dots"),
          ("John_Smith", RandomData.get_password(), "USER", RandomData.get_name(),"username","Username must contain only letters, digits, dashes, underscores, and dots"),
          ("John-Smith", RandomData.get_password(), "USER", RandomData.get_name(),"username","Username must contain only letters, digits, dashes, underscores, and dots"),
          ("John Smilk th ", RandomData.get_password(), "USER", RandomData.get_name(),"username","Username must contain only letters, digits, dashes, underscores, and dots"),

          ],)
    def test_invalid_update_profile_name(self, username, password, role, name,error_key, error_value):
        create_user_request = CreateUserRequest(
            username=username, password=password, role=role)
        create_user_response = AdminUserRequester(
        RequestSpec.admin_auth_spec(),
        ResponseSpec.entity_was_created()
        ).post(create_user_request)

        assert create_user_response.username == create_user_request.username

        login_user_request = LoginUserRequest(
            username=username, password=password)
        login_user_response = LoginUserRequester(
            RequestSpec.unauth_spec(),
            ResponseSpec.request_return_ok()
            ).post(login_user_request)

        assert login_user_request.username == login_user_response.username


        update_profile_payload = UpdateProfileRequest(name=name)
        update_profile_response = UpdateProfileRequester(
            RequestSpec.user_auth_spec(username, password),
            ResponseSpec.request_return_ok(),
        ).put(payload.model_dump())

        response = UpdateProfileRequester(
            user_auth["spec"],
            ResponseSpec.request_return_bad_response(error_key, error_value),
        ).put(payload.model_dump())

        assert update_profile_response.customer.get(
            "name") == login_user_response.username



        logger.info( f"[Invalid Profile Attempt] name={name}, response={response}")
