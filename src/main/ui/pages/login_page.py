from playwright.sync_api import Page

class LoginPage:
   
    def __init__(self, page:Page):
        self.page = page
        self.username_form = page.get_by_placeholder('Username')
        self.password_form = page.get_by_placeholder('Password')
        self.login_button = page.locator("button:has-text('Login')")

    def login(self, username, password):
        self.username_form.fill(username)
        self.password_form.fill(password)
        self.login_button.click()
        return self

        


        



