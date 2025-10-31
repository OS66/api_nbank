
import pytest
import logging

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

from src.main.api.generators.random_data import RandomData


class TestTransfer:

    @pytest.mark.trans
    @pytest.mark.parametrize("username, password, role, amount,  transfer_amount",
                             [(RandomData.get_username(), RandomData.get_password(), "USER", 400.0, 300.5)])
    def test_create_transfer(self, username, password, role, amount, transfer_amount):
        create_user_request = CreateUserRequest(
            username=username, password=password, role=role)
        create_user_response = AdminUserRequester(
            RequestSpec.admin_auth_spec(),
            ResponseSpec.entity_was_created()
        ).post(create_user_request)

        assert create_user_response.username == create_user_request.username
        assert create_user_response.role == create_user_request.role

        source_account_response = CreateAccountRequester(
            RequestSpec.user_auth_spec(
                create_user_request.username, create_user_request.password),
            ResponseSpec.entity_was_created(),
        ).post()
        assert source_account_response.balance == 0.0

        target_account_response = CreateAccountRequester(
            RequestSpec.user_auth_spec(
                create_user_request.username, create_user_request.password),
            ResponseSpec.entity_was_created(),
        ).post()
        assert target_account_response.balance == 0.0

        source_account_id = source_account_response.id
        target_account_id = target_account_response.id
        logging.info(
            f'first account id: {source_account_response.id} second   accound id: {target_account_response.id}')

        deposit_request = CreateDepositRequest(
            id=source_account_id, balance=amount)
        CreateDepositRequester(
            RequestSpec.user_auth_spec(username, password),
            ResponseSpec.request_return_ok(),
        ).post(deposit_request)

        transfer_request = CreateTransferRequest(
            senderAccountId=source_account_id,
            receiverAccountId=target_account_id,
            amount=transfer_amount,
        )

        transfer_response = CreateTransferRequester(
            RequestSpec.user_auth_spec(username, password),
            ResponseSpec.request_return_ok(),
        ).post(transfer_request)

        assert transfer_response.get('amount') == transfer_amount

        logging.info(
            f'Transfer from account id: {source_account_response.id}, amount {amount} to  the  second accound id: {target_account_response.id}  with {transfer_amount} ')

        transactions = GetTransactionsRequester(
            RequestSpec.user_auth_spec(username, password),
            ResponseSpec.request_return_ok(),
        ).get(source_account_id)

        assert isinstance(transactions, list)
        assert any(t.get("amount") == transfer_amount for t in transactions)

        logging.info(f'List og transactions {transactions}')

    @pytest.mark.trans_invalid
    @pytest.mark.parametrize(
        "username, password, role, amount, transfer_amount, error_key, error_value",
        [
            ( RandomData.get_username(),RandomData.get_password(),"USER",200.0,340.0,"message", "Invalid transfer: insufficient funds or invalid accounts",
            ),
            (RandomData.get_username(),RandomData.get_password(),"USER",10080,1000.70,"message", "Invalid transfer: insufficient funds or invalid accounts",
            ),
            (RandomData.get_username(), RandomData.get_password(),"USER",20,0, "message","Invalid transfer: insufficient funds or invalid accounts",
            ),
        ],
    )
    def test_create_invalid_transfer(self, username, password, role, amount, transfer_amount, error_key, error_value):
        create_user_request = CreateUserRequest(
            username=username, password=password, role=role)
        create_user_response = AdminUserRequester(
            RequestSpec.admin_auth_spec(),
            ResponseSpec.entity_was_created()
        ).post(create_user_request)

        assert create_user_response.username == create_user_request.username
        assert create_user_response.role == create_user_request.role

        source_account_response = CreateAccountRequester(
            RequestSpec.user_auth_spec(
                create_user_request.username, create_user_request.password),
            ResponseSpec.entity_was_created(),
        ).post()
        assert source_account_response.balance == 0.0

        target_account_response = CreateAccountRequester(
            RequestSpec.user_auth_spec(
                create_user_request.username, create_user_request.password),
            ResponseSpec.entity_was_created(),
        ).post()
        assert target_account_response.balance == 0.0

        source_account_id = source_account_response.id
        target_account_id = target_account_response.id
        logging.info(
            f'first account id: {source_account_response.id} second accound id: {target_account_response.id}')

        deposit_request = CreateDepositRequest(
            id=source_account_id, balance=amount)
        CreateDepositRequester(
            RequestSpec.user_auth_spec(username, password),
            ResponseSpec.request_return_ok(),
        ).post(deposit_request)

        transfer_request = CreateTransferRequest(
            senderAccountId=source_account_id,
            receiverAccountId=target_account_id,
            amount=transfer_amount,
        )

        transfer_response = CreateTransferRequester(
            RequestSpec.user_auth_spec(username, password),
            ResponseSpec.request_return_bad_request(error_key, error_value),
        ).post(transfer_request)

        logging.info(
            f'Transfer from account id: {source_account_response.id}, amount {amount} to  the  second accound id: {target_account_response.id}  with {transfer_amount} ')
