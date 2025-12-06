import pytest
import logging


from src.main.api.generators.random_data import RandomData
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.specs.response_spec import ResponseSpec

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse



from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.requests.create_account_requester import CreateAccountRequester

from src.main.api.requests.admin_user_requester import AdminUserRequester

from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.login_user_requester import LoginUserRequester

from src.main.api.requests.create_deposit_requester import CreateDepositRequester
from src.main.api.models.create_deposit_request import CreateDepositRequest
from src.main.api.models.create_deposit_response import CreateDepositResponse
from src.main.constants.roles import Roles

class TestDeposit():

    @pytest.mark.deposit
    @pytest.mark.parametrize(
        "username, password, role, balance",
        [(
            RandomData.get_username(),RandomData.get_password(),Roles.USER, RandomData.get_balance()
        )])
    def test_create_valid_deposit(self, username, password, role, balance):
        create_user_request = CreateUserRequest(username=username, password=password, role=role)
        create_user_response = AdminUserRequester(
            RequestSpec.admin_auth_spec(),
            ResponseSpec.entity_was_created()
        ).post(create_user_request)

        assert create_user_response.username == create_user_request.username
        logging.info(f'User created "{create_user_request.username}" with password:  {create_user_request.password}')


        create_account_response = CreateAccountRequester(
            RequestSpec.user_auth_spec(create_user_request.username, create_user_request.password),
            ResponseSpec.entity_was_created()
        ).post()

        assert create_account_response.balance == 0.0
      
        create_deposit_request = CreateDepositRequest(
            id=create_account_response.id,
            balance=balance
        )
        create_deposit_response = CreateDepositRequester(
            RequestSpec.user_auth_spec(username, password),
            ResponseSpec.request_return_ok()
        ).post(create_deposit_request)

        assert create_deposit_response.balance == create_deposit_request.balance
        logging.info(f'Valid deposit with response  for "{create_deposit_response.balance}" amount for  "{create_user_request.username}" user')





    @pytest.mark.deposit
    @pytest.mark.parametrize(
        "username, password, role, balance,error_key, error_value",
       [
         (RandomData.get_username(), RandomData.get_password(), Roles.USER, -508, 'balance', "Invalid account or amount"),
         (RandomData.get_username(), RandomData.get_password(), Roles.USER, "test", None, "Internal Server Error"),
                                                                                                     ],
        )
    def test_create_invalid_deposit(self, username, password, role, balance, error_key, error_value):

        create_user_request = CreateUserRequest(username=username, password=password, role=role)
        create_user_response = AdminUserRequester(
            RequestSpec.admin_auth_spec(),
            ResponseSpec.entity_was_created()
        ).post(create_user_request)

        assert create_user_response.username == create_user_request.username

        create_account_response = CreateAccountRequester(
            RequestSpec.user_auth_spec(create_user_request.username, create_user_request.password),
            ResponseSpec.entity_was_created()
        ).post()


        assert create_account_response.balance == 0.0
      
        create_deposit_request = CreateDepositRequest(
            id=create_account_response.id,
            balance=balance
        )

        create_deposit_response = CreateDepositRequester(
            RequestSpec.user_auth_spec(username, password),
            ResponseSpec.request_return_bad_request(error_key, error_value)
        ).post(create_deposit_request)

        assert create_user_response.username == create_user_request.username


       



        

     
