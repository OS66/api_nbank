from playwright.sync_api import sync_playwright
import pytest
import logging

from src.main.api.generators.random_data import RandomData
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.get_accounts_requester import GetAccountsRequester
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.models.create_user_request import CreateUserRequest


class TestCreateAccount:
    BASE_URL = 'http://localhost:3000/'

    
    def test_user_create_account(self):
        # login  admin - шаг настройки
        # admin create  user- - шаг настройки
        # user log in- - шаг настройки

        username = RandomData.get_username()
        password = RandomData.get_password()
        role = "USER"

        create_user_request = CreateUserRequest(username=username, password=password, role=role)
        create_user_response = AdminUserRequester(
            RequestSpec.admin_auth_spec(),
            ResponseSpec.entity_was_created()
        ).post(create_user_request)

        assert create_user_response.username == create_user_request.username

        # login and create account - шаг теста
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url=self.BASE_URL)

            page.get_by_placeholder('Username').fill(username)
            page.get_by_placeholder('Password').fill(password)

            logging.info(f"\nUser created  and loged in:\n\n{username} and {password}\n ")
            page.locator("button:has-text('Login')").click()

            create_button = page.locator("button:has-text('Create New Account')")
            create_button.wait_for()

            with page.expect_event("dialog") as dialog_info:
                create_button.click()

            dialog = dialog_info.value
            message = dialog.message
            logging.info(message)
            
            assert "New Account Created!" in message
            dialog.accept()

            account_number = None
            if "Account Number:" in message:
                account_number = message.split("Account Number:")[-1].strip()
            logging.info(f"Account number: {account_number}")

            browser.close()
