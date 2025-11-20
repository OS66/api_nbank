from playwright.sync_api import sync_playwright
import pytest
import logging
import time




class TestLogin:
    BASE_URL = 'http://localhost:3000/'

    
    def test_admin_login(self, admin_credentials):
        adm_username, adm_password = admin_credentials
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url=self.BASE_URL)

            assert page.title() == 'NoBugs Bank'

            logging.info(f"\nThere is a Title : {page.title()}\n")
            username_form = page.get_by_placeholder('Username').fill(adm_username)
            password_form = page.get_by_placeholder('Password').fill(adm_password)
            login_button = page.locator("button:has-text('Login')").click()
          
            page.get_by_text('Admin Panel').wait_for()


            browser.close()


   
    def test_user_login(self, user_credentials):
        user_username, user_password = user_credentials
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

            assert page.get_by_text('title')

            name = page.locator(".welcome-text:has-text('Welcome, noname')")
            time.sleep(2)
            assert name.is_visible()

            browser.close()



    