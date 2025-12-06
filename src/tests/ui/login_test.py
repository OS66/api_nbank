from playwright.sync_api import sync_playwright
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.user_panel import UserPanel
from src.main.ui.pages.admin_panel import AdminPanel

import pytest
import logging
import time


class TestLogin:
    
    def test_admin_login(self, admin_credentials, page):

        adm_username, adm_password = admin_credentials
        assert page.title() == 'NoBugs Bank'

        LoginPage(page).login(adm_username,adm_password)
        AdminPanel(page).check_admin_title()

        assert AdminPanel(page).title.is_visible()


   
    def test_user_login(self, user_credentials, page):
        user_username, user_password = user_credentials
        assert page.title() == 'NoBugs Bank'
        LoginPage(page).login(user_username,user_password)
        UserPanel(page).check_title_noname()

        assert UserPanel(page).noname_title.is_visible()

        



    