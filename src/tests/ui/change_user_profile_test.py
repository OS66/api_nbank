from playwright.sync_api import sync_playwright
import pytest
import logging

import time

from src.main.api.generators.random_data import RandomData



class TestUpdateProfileUI():
     BASE_URL = 'http://localhost:3000/'
    
     @pytest.mark.utest
     def test_valid_update_profile(self, user_credentials):
        user_username, user_password = user_credentials
        new_name = RandomData.get_name()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url=self.BASE_URL)

            assert page.title() == 'NoBugs Bank'

            username_form = page.get_by_placeholder('Username').fill(user_username)
           
            password_form = page.get_by_placeholder('Password').fill(user_password)
            login_button = page.locator("button:has-text('Login')").click()
            logging.info(f"\nUser created  and loged in:\n\n{user_username} and {user_password}\n ")
            # time.sleep(4)
            title = "User Dashboard"

            page.get_by_text(title).wait_for()

            name = page.locator(".welcome-text:has-text('Welcome, noname')")
           
            assert name.is_visible()
            logging.info(new_name)

            page.locator(".user-name", has_text="Noname").click()
            page.get_by_placeholder("Enter new name").fill(new_name)

            btn_save = page.locator("button:has-text('💾 Save Changes')")
           

            with page.expect_event("dialog") as dialog_info:
                btn_save.click()

                 
            dialog = dialog_info.value
            message = dialog.message
            logging.info(message)

            assert "Name updated successfully!" in message

            dialog.accept()
           

            btn_home = page.locator("button:has-text('🏠 Home')")
            btn_home.click()
           
            name = page.locator(f".welcome-text:has-text('Welcome, {new_name}')")
            name.wait_for()

            message = page.locator('h2').text_content()
            logging.info(message)


            browser.close()




    


        



