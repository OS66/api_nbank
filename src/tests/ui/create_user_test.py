from playwright.sync_api import sync_playwright
import pytest
import logging


from src.main.api.generators.random_data import RandomData
from src.main.api.configs.config import Config
from src.main.api.requests.get_profile_requester import GetProfileRequester
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.specs.response_spec import ResponseSpec

from src.main.constants.roles import Roles
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.user_panel import UserPanel
from src.main.ui.pages.admin_panel import AdminPanel


class TestCreateUser:
    @pytest.mark.test3
    def test_admin_create_user(self, admin_credentials, page):
        #UI login  admin
        adm_username, adm_password = admin_credentials
        user_username = RandomData.get_username()
        user_password = RandomData.get_password()
        
        LoginPage(page).login(adm_username,adm_password)
        AdminPanel(page).check_admin_title()
        assert AdminPanel(page).title.is_visible()

         #UI steps admin  create a user
        message  = AdminPanel(page).create_user(user_username,user_password)
        assert message == "✅ User created successfully!"
        # assert user_panel.noname_title.is_visible()

        #ui check    
        page.goto(Config.get("frontendUrl"))
        LoginPage(page).login(user_username, user_password)
        user_panel = UserPanel(page).check_title_noname()
        assert user_panel.noname_title.is_visible()


    def test_admin_create_invalid_user(self, admin_credentials, page):
        # login  admin
        adm_username, adm_password = admin_credentials
        
        login_page = LoginPage(page)
        login_page.login(adm_username,adm_password)
        admin_panel = AdminPanel(page)
        admin_panel.check_admin_title()
      
        title_create_user = admin_panel.create_user_title
        title_create_user.wait_for()
        assert title_create_user.is_visible()

        # admin  create a user2
        user_username = 'R9090 09_%()'
        user_password = '*'

        admin_panel.fill_create_user_form(user_username,user_password)

        # check the alert3
        with page.expect_event("dialog") as dialog_info:
                admin_panel.submit_create_user_form()

        dialog = dialog_info.value
        message = dialog.message

        assert "Failed to create user" in message
        assert "Password must contain at least one digit" in message
        assert "Username must contain only letters, digits, dashes, underscores, and dots" in message

        dialog.accept()

        # check that user was NoT creted on UI
        assert page.locator(f"li:has-text('{user_username}')").count() == 0
