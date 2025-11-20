
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

class TestCreateDeposit():
    BASE_URL = 'http://localhost:3000/'

    
    def test_create_deposit(self):
        username = RandomData.get_username()
        password = RandomData.get_password()
        role = "USER"
        balance = str(RandomData.get_balance())
        
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


        # ui login
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url=self.BASE_URL)
            assert page.title() == 'NoBugs Bank'

            page.get_by_placeholder('Username').fill(username)
            page.get_by_placeholder('Password').fill(password)
            page.locator("button:has-text('Login')").click()
            logging.info(f"\nUser created  and loged in:\n\n{username} and {password}\n ")
            title = "User Dashboard"
            page.get_by_text(title).wait_for()

            deposit_button = page.get_by_role("button", name="💰 Deposit Money", exact=True).click()
          

            page.select_option(
                "select.account-selector",
                page.locator("select.account-selector option").nth(1).get_attribute("value")
            )

            page.locator("input.deposit-input").fill(balance)
            deposit_submit = page.get_by_role("button", name="💵 Deposit", exact=True)
            deposit_submit.wait_for(state="visible")

            with page.expect_event("dialog") as dialog_info:
                deposit_submit.click()

                 
            dialog = dialog_info.value
            message = dialog.message
            logging.info(message)

            assert "Successfully deposited" in message
            
            dialog.accept()
            browser.close()


    @pytest.mark.invalidd
    def test_create_invalid_deposit(self):
        username = RandomData.get_username()
        password = RandomData.get_password()
        role = "USER"
        balance = '799900'
        
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

        # ui login
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url=self.BASE_URL)
            assert page.title() == 'NoBugs Bank'

            page.get_by_placeholder('Username').fill(username)
            page.get_by_placeholder('Password').fill(password)
            page.locator("button:has-text('Login')").click()
            logging.info(f"\nUser created  and loged in:\n\n{username} and {password}\n ")
            title = "User Dashboard"
            page.get_by_text(title).wait_for()

            deposit_btn= page.get_by_role("button", name="💰 Deposit Money", exact=True)
            
            deposit_btn.click()

            page.select_option(
                "select.account-selector",
                page.locator("select.account-selector option").nth(1).get_attribute("value")
            )

            page.locator("input.deposit-input").fill(balance)

     
            page.get_by_role("button", name="💵 Deposit").click()

            with page.expect_event("dialog") as dialog_info:
                deposit_submit.click()

                 
            dialog = dialog_info.value
            message = dialog.message
            logging.info(message)

            assert "Please deposit less or equal to 5000$" in dialog.message
            
            dialog.accept()
            browser.close()







            
