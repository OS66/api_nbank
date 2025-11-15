# import pytest

# from src.main.api.requests.admin_user_requester import AdminUserRequester
# from src.main.api.requests.login_user_requester import LoginUserRequester
# from src.main.api.specs.request_spec import RequestSpec
# from src.main.api.specs.response_spec import  ResponseSpec
# from src.main.api.generators.random_data import RandomData
# from src.main.api.models.create_user_request import CreateUserRequest
# from src.main.api.models.login_user_request import LoginUserRequest



# @pytest.fixture
# def user_auth():
#     username = RandomData.get_username()
#     password = RandomData.get_password()
#     AdminUserRequester(
#         RequestSpec.admin_auth_spec(),
#         ResponseSpec.entity_was_created()
#     ).post(CreateUserRequest(username=username, password=password, role="USER"))

#     LoginUserRequester(
#         RequestSpec.unauth_spec(),
#         ResponseSpec.request_return_ok()
#     ).post(LoginUserRequest(username=username, password=password))

#     return {
#         "username": username,
#         "password": password,
#         "auth_spec": RequestSpec.user_auth_spec(username, password),
#     }
