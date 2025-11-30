from playwright.sync_api import Page

class UserPanel:
    def __init__(self,page: Page):
        self.page = page

    @property
    def title(self):
        return self.page.get_by_text("User Dashboard")
        
    @property
    def noname_title(self):
        return self.page.locator(".welcome-text:has-text('Welcome, noname')")

    def check_title_noname(self):
        self.title.wait_for()
        self.noname_title.wait_for()
        return self     

    def update_name(self, new_name: str):
        self.page.locator(".user-name", has_text="Noname").click()
        self.page.get_by_placeholder("Enter new name").fill(new_name)
        btn_save = self.page.locator("button:has-text('💾 Save Changes')")
    
        with self.page.expect_event("dialog") as dialog_info:
            btn_save.click()

        dialog = dialog_info.value
        message = dialog.message
        dialog.accept()
        return message

    def check_updated_name(self, new_name):
        btn_home = self.page.locator("button:has-text('🏠 Home')")
        btn_home.click()
        name = self.page.locator(f".welcome-text:has-text('Welcome, {new_name}')")
        name.wait_for()
        message = self.page.locator('h2').text_content()
        return message

    def create_account(self):
        create_button = self.page.locator("button:has-text('Create New Account')")
        create_button.wait_for()

        with self.page.expect_event("dialog") as dialog_info:
            create_button.click()

        dialog = dialog_info.value
        message = dialog.message
        dialog.accept() 
        return message   

    def check_account_number(self, message: str):
        account_number = message.split("Account Number:")[-1].strip()
        number_digits = "".join(filter(str.isdigit, account_number))
        return int(number_digits)

    def create_deposit(self, balance):
        deposit_button = self.page.get_by_role("button", name="💰 Deposit Money", exact=True).click()
        
        self. page.select_option(
             "select.account-selector",
            self.page.locator("select.account-selector option").nth(1).get_attribute("value")
        )

        self.page.locator("input.deposit-input").fill(balance)
        deposit_submit = self.page.get_by_role("button", name="💵 Deposit", exact=True)
        deposit_submit.wait_for(state="visible")

        with self.page.expect_event("dialog") as dialog_info:
            deposit_submit.click()

        dialog = dialog_info.value
        message = dialog.message
        dialog.accept()  
        return message  


    def make_transfer(self, source_account_id:int, target_account_id:int, transfer_amount):
        transfer_submit = self.page.get_by_role("button", name="🔄 Make a Transfer", exact=True).click()
        self.page.select_option("select.account-selector",str(source_account_id))
        self.page.get_by_placeholder("Enter recipient name").fill('Name check')
        self.page.get_by_placeholder("Enter recipient account number").fill(str(target_account_id))
        self.page.get_by_placeholder("Enter amount").fill(str(transfer_amount))
        self.page.locator("#confirmCheck").check()

        btn_transfer = self.page.get_by_role("button", name="🚀 Send Transfer")

        with self.page.expect_event("dialog") as dialog_info:
            btn_transfer.click()

        dialog = dialog_info.value
        message = dialog.message

        dialog.accept()
        return message



         

      
