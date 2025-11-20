from playwright.sync_api import sync_playwright
import pytest
import logging


from src.main.api.generators.random_data import RandomData
from src.main.api.requests.get_profile_requester import GetProfileRequester
from src.main.api.specs.request_spec import RequestSpec
from src.main.api.specs.response_spec import ResponseSpec


class TestCreateUser:
    BASE_URL = 'http://localhost:3000/'

    
    def test_admin_create_user(self, admin_credentials):
        #login  admin1
        adm_username, adm_password = admin_credentials
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url=self.BASE_URL)

            username_form = page.get_by_placeholder('Username').fill(adm_username)
            password_form = page.get_by_placeholder('Password').fill(adm_password)
            
            login_button = page.locator("button:has-text('Login')").click()        
           
            title_create_user = page.locator("h2:has-text('Create New User')")
            title_create_user.wait_for()
            assert title_create_user.is_visible()

            #admin  create a user2
            user_username = RandomData.get_username()
            user_password = RandomData.get_password()

            username_form = page.get_by_placeholder('Username').fill(user_username)
            password_form = page.get_by_placeholder('Password').fill(user_password)
            # time.sleep(10)
           
           #check the alert3
            with page.expect_event("dialog") as dialog_info:
                 page.get_by_role("button", name="Add User").click()
            dialog = dialog_info.value
            
            assert dialog.message ==  "✅ User created successfully!"

            logging.info({dialog.message})

            dialog.accept()

            #check that user was creted on UI 
            page.locator(f"ul.card.shadow-custom li:has-text('{user_username}')").wait_for(timeout=9000)
            assert page.locator(f"li:has-text('{user_username}')").is_visible()

            #ui
            profile = GetProfileRequester(
                        RequestSpec.user_auth_spec(user_username, user_password),
                        ResponseSpec.request_return_ok()
                    ).get()
            assert profile.username == user_username

            browser.close()




    
    def test_admin_create_invalid_user(self, admin_credentials):
        #login  admin1
        adm_username, adm_password = admin_credentials
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url=self.BASE_URL)

            username_form = page.get_by_placeholder('Username').fill(adm_username)
            password_form = page.get_by_placeholder('Password').fill(adm_password)
            
            login_button = page.locator("button:has-text('Login')").click()        
           
            title_create_user = page.locator("h2:has-text('Create New User')")
            title_create_user.wait_for()
            assert title_create_user.is_visible()

            #admin  create a user2
            user_username = 'R9090 09_%()'
            user_password = '*'

            username_form = page.get_by_placeholder('Username').fill(user_username)
            password_form = page.get_by_placeholder('Password').fill(user_password)

            #check the alert3
            with page.expect_event("dialog") as dialog_info:
                 page.get_by_role("button", name="Add User").click()
                 
            dialog = dialog_info.value
            message = dialog.message
            logging.info(message)

            assert "Failed to create user" in message
            assert "Password must contain at least one digit" in message
            assert "Username must contain only letters, digits, dashes, underscores, and dots" in message

            dialog.accept()


            #check that user was NoT creted on UI 
            assert page.locator(f"li:has-text('{user_username}')").count() == 0








           

           










            browser.close()
