from playwright.sync_api import sync_playwright
import pytest
import logging

from src.main.api.generators.random_data import RandomData
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.get_accounts_requester import GetAccountsRequester
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.models.create_user_request import CreateUserRequest


from src.main.constants.roles import Roles
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.user_panel import UserPanel
from src.main.ui.pages.admin_panel import AdminPanel


class TestCreateAccount:
    def test_user_create_account(self, page):
        # login  admin - шаг настройки
        # admin create  user- - шаг настройки
        # user log in- - шаг настройки

        username = RandomData.get_username()
        password = RandomData.get_password()
        role = Roles.USER

        create_user_request = CreateUserRequest(username=username, password=password, role=role)
        create_user_response = AdminUserRequester(
            RequestSpec.admin_auth_spec(),
            ResponseSpec.entity_was_created()
        ).post(create_user_request)

        assert create_user_response.username == create_user_request.username

        # login and create account - шаг теста
        LoginPage(page).login(username,password)
        user_panel = UserPanel(page).check_title_noname()

        message = user_panel.create_account()
        assert "New Account Created!" in message
        logging.info(message)

        account_number = user_panel.check_account_number(message)
        logging.info(account_number)
        assert account_number > 0


  
