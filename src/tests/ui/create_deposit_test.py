
from playwright.sync_api import sync_playwright
import pytest
import logging
import time

from src.main.api.generators.random_data import RandomData
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.specs.response_spec import ResponseSpec

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.admin_user_requester import AdminUserRequester

from src.main.constants.roles import Roles
from src.main.ui.pages.login_page import LoginPage
from src.main.constants.error_messagess import Errors
from src.main.ui.pages.user_panel import UserPanel
from src.main.ui.pages.admin_panel import AdminPanel


class TestCreateDeposit:

    def test_create_deposit(self, page):
        username = RandomData.get_username()
        password = RandomData.get_password()
        role = Roles.USER
        balance = str(RandomData.get_balance())
        
        #api
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


        # ui login
     
        assert page.title() == 'NoBugs Bank'

        LoginPage(page).login(username,password)
        user_panel = UserPanel(page).check_title_noname()
        message  = user_panel.create_deposit(balance)

        assert Success.SUCCESS_DEPOSITED in message, "There is no 'Successfully deposited' message "



    
    def test_create_invalid_deposit(self, page):
        username = RandomData.get_username()
        password = RandomData.get_password()
        role = Roles.USER
        balance = str(RandomData.get_invalid_balance())
        
        #api
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

        assert page.title() == 'NoBugs Bank'



        # ui login
     
        assert page.title() == 'NoBugs Bank'

        LoginPage(page).login(username,password)
        user_panel = UserPanel(page).check_title_noname()
        message  = user_panel.create_deposit(balance)
        assert Errors.ERROR_DEPOSIT_LIMIT in message, "Message was not as expected"
       






            
