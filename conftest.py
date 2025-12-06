import pytest
from playwright.sync_api import sync_playwright

from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.specs.response_spec import  ResponseSpec
from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.configs.config import Config



@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(Config.get("frontendUrl"))
        yield page
        page.close()
        browser.close()


@pytest.fixture(scope="session")
def admin_credentials():
    adm_username = "admin"
    adm_password = "admin"
    return adm_username, adm_password 
   

@pytest.fixture(scope="session")
def user_credentials():
    username = RandomData.get_username()
    password = RandomData.get_password()
    create_user_request = CreateUserRequest(
        username=username,
        password= password,
        role="USER"
    )
    AdminUserRequester(RequestSpec.admin_auth_spec(),
    ResponseSpec.entity_was_created()).post(create_user_request)
    return username, password
