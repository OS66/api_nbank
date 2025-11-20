
import pytest
import logging
import time

from playwright.sync_api import sync_playwright

from src.main.api.requests.get_profile_requester import GetProfileRequester
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.specs.response_spec import ResponseSpec

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.requests.create_deposit_requester import CreateDepositRequester
from src.main.api.models.create_deposit_request import CreateDepositRequest

from src.main.api.models.create_transfer import CreateTransferRequest
from src.main.api.requests.create_transfer_requester import CreateTransferRequester
from src.main.api.requests.get_transactions_requester import GetTransactionsRequester

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.get_accounts_requester import GetAccountsRequester

from src.main.api.generators.random_data import RandomData


class TestTransferUI:
    BASE_URL = 'http://localhost:3000/'

    @pytest.mark.uis
    @pytest.mark.parametrize("username, password, role, amount,  transfer_amount",
                             [(RandomData.get_username(), RandomData.get_password(), "USER", 600, 105)])
    def test_create_transfer(self, username, password, role, amount, transfer_amount):
    

        create_user_request = CreateUserRequest(username=username, password=password, role=role)
        create_user_response = AdminUserRequester(
            RequestSpec.admin_auth_spec(),
            ResponseSpec.entity_was_created()).post(create_user_request)

        assert create_user_response.username == create_user_request.username
        assert create_user_response.role == create_user_request.role

        source_account_response = CreateAccountRequester(
            RequestSpec.user_auth_spec(
                create_user_request.username, create_user_request.password),
            ResponseSpec.entity_was_created(),).post()
        assert source_account_response.balance == 0.0

        target_account_response = CreateAccountRequester(
            RequestSpec.user_auth_spec(
                create_user_request.username, create_user_request.password),
            ResponseSpec.entity_was_created(),).post()
        assert target_account_response.balance == 0.0

        source_account_id = source_account_response.id 
        target_account_id = target_account_response.id
        logging.info(f'first account id: {source_account_response.id} second   accound id: {target_account_response.id}')
        
        #new deposit
        deposit_request = CreateDepositRequest(id=source_account_id, balance=amount)
        CreateDepositRequester(
            RequestSpec.user_auth_spec(username, password),
            ResponseSpec.request_return_ok(),).post(deposit_request)
        assert deposit_request.balance == amount

        #check deposit
        response_get_deposit= GetAccountsRequester(
            RequestSpec.user_auth_spec(username,password),
            ResponseSpec.request_return_ok()).get()

        logging.info(f'response_get_deposit~!!!!!!!!: {response_get_deposit.dict()}')


        start_balances= {}
        for i in response_get_deposit.accounts:
            account_id =  i['id']
            account_balance = i['balance']
            start_balances[account_id] = account_balance 

        assert start_balances[source_account_id] == deposit_request.balance


        #new transfer UI - login
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url=self.BASE_URL)

            assert page.title() == 'NoBugs Bank'

            username_form = page.get_by_placeholder('Username').fill(username)
           
            password_form = page.get_by_placeholder('Password').fill(password)
            login_button = page.locator("button:has-text('Login')").click()
            logging.info(f"\nUser created  and loged in:\n\n{username} and {password}\n ")
            # time.sleep(4)
            title = "User Dashboard"

            assert page.get_by_text('title')

            name = page.locator(".welcome-text:has-text('Welcome, noname')")
            time.sleep(2)
            assert name.is_visible()

            transfer_submit = page.get_by_role("button", name="🔄 Make a Transfer", exact=True).click()
           
            
            page.select_option("select.account-selector", str(source_account_id))

            # page.locator("input").fill('50')
            page.get_by_placeholder("Enter recipient name").fill('Name check')
            page.get_by_placeholder("Enter recipient account number").fill(str(target_account_id))
            page.get_by_placeholder("Enter amount").fill('50')
            # source_account_id 
            # target_account_id 
           
            page.locator("#confirmCheck").check()

            btn_transfer = page.get_by_role("button", name="🚀 Send Transfer")

            with page.expect_event("dialog") as dialog_info:
                btn_transfer.click()
                 
            dialog = dialog_info.value
            message = dialog.message
            logging.info(message)

            assert "Trannfer success" in message
            dialog.accept()

            browser.close()

            





        




        







    # @pytest.mark.trans_invalid
    # @pytest.mark.parametrize(
    #     "username, password, role, amount, transfer_amount, error_key, error_value",
    #     [
    #         ( RandomData.get_username(),RandomData.get_password(),"USER",200.0,340.0,"message", "Invalid transfer: insufficient funds or invalid accounts",
    #         ),
    #         (RandomData.get_username(),RandomData.get_password(),"USER",10080,1000.70,"message", "Invalid transfer: insufficient funds or invalid accounts",
    #         ),
    #         (RandomData.get_username(), RandomData.get_password(),"USER",20,0, "message","Invalid transfer: insufficient funds or invalid accounts",
    #         ),
    #     ],
    # )
    # def test_create_invalid_transfer(self, username, password, role, amount, transfer_amount, error_key, error_value):
    #     create_user_request = CreateUserRequest(
    #         username=username, password=password, role=role)
    #     create_user_response = AdminUserRequester(
    #         RequestSpec.admin_auth_spec(),
    #         ResponseSpec.entity_was_created()
    #     ).post(create_user_request)

    #     assert create_user_response.username == create_user_request.username
    #     assert create_user_response.role == create_user_request.role

    #     source_account_response = CreateAccountRequester(
    #         RequestSpec.user_auth_spec(
    #             create_user_request.username, create_user_request.password),
    #         ResponseSpec.entity_was_created(),
    #     ).post()
    #     assert source_account_response.balance == 0.0

    #     target_account_response = CreateAccountRequester(
    #         RequestSpec.user_auth_spec(
    #             create_user_request.username, create_user_request.password),
    #         ResponseSpec.entity_was_created(),
    #     ).post()
    #     assert target_account_response.balance == 0.0

    #     source_account_id = source_account_response.id
    #     target_account_id = target_account_response.id
    #     logging.info(
    #         f'first account id: {source_account_response.id} second accound id: {target_account_response.id}')

    #     deposit_request = CreateDepositRequest(
    #         id=source_account_id, balance=amount)
    #     CreateDepositRequester(
    #         RequestSpec.user_auth_spec(username, password),
    #         ResponseSpec.request_return_ok(),
    #     ).post(deposit_request)

    #     transfer_request = CreateTransferRequest(
    #         senderAccountId=source_account_id,
    #         receiverAccountId=target_account_id,
    #         amount=transfer_amount,
    #     )

    #     transfer_response = CreateTransferRequester(
    #         RequestSpec.user_auth_spec(username, password),
    #         ResponseSpec.request_return_bad_request(error_key, error_value),
    #     ).post(transfer_request)

    #     logging.info(
    #         f'Transfer from account id: {source_account_response.id}, amount {amount} to  the  second accound id: {target_account_response.id}  with {transfer_amount} ')
