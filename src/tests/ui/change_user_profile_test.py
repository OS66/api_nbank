from playwright.sync_api import sync_playwright
import pytest
import logging

import time

from src.main.api.generators.random_data import RandomData
from src.main.constants.roles import Roles
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.user_panel import UserPanel



class TestUpdateProfileUI:
    
     def test_update_profile(self, user_credentials, page):
        user_username, user_password = user_credentials
        new_name = RandomData.get_name()

        assert page.title() == 'NoBugs Bank'

        LoginPage(page).login(user_username,user_password)
        
        user_panel=UserPanel(page).check_title_noname()

        message_updated  = user_panel.update_name(new_name)
        assert "Name updated successfully!" in message_updated

        message = user_panel.check_updated_name(new_name)
        assert new_name in message 



     




    


        



