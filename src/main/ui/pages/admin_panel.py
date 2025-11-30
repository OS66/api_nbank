
from playwright.sync_api import Page

class AdminPanel:
    def __init__(self,page: Page):
        self.page = page

    @property
    def title(self):
        return self.page.get_by_text("Admin Panel")

    @property
    def create_user_title(self):
        return self.page.locator("h2:has-text('Create New User')")

    @property
    def _create_user_section(self):
        return self.page.locator("xpath=//h2[contains(normalize-space(), 'Create New User')]/..")

    @property
    def create_user_username_input(self):
        return self._create_user_section.get_by_placeholder("Username")

    @property
    def create_user_password_input(self):
        return self._create_user_section.get_by_placeholder("Password")

    @property
    def create_user_button(self):
        return self._create_user_section.get_by_role("button", name="Add User")

    def check_admin_title(self):
         self.title.wait_for()
         return self

    def create_user(self, username: str, password: str):
        self.create_user_username_input.fill(username)
        self.create_user_password_input.fill(password)

        with self.page.expect_event("dialog") as dialog_info:
            self.create_user_button.click()

        dialog = dialog_info.value
        message = dialog.message
        dialog.accept()

        return message



    def wait_for_user_in_list(self, username: str):
        locator = self.page.locator(f"ul.card.shadow-custom li:has-text('{username}')")
        locator.wait_for(timeout=9000)
        return locator

      
