from driver import Driver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import time

load_dotenv()


class CEIWordPress(Driver):

    def __init__(self):
        super().__init__()
        self.url = os.environ.get("WP_URL")

    def login(self):
        username_field = self.driver.find_element(By.ID, "user_login")
        username_field.send_keys(os.environ.get("WP_USERNAME"))
        password_field = self.driver.find_element(By.ID, "user_pass")
        password_field.send_keys(os.environ.get("WP_PASSWORD"))
        self.driver.find_element(By.ID, "wp-submit").click()

    def post_events(self):
        self.driver.get(self.url)
        self.login()
        time.sleep(2.5)
        ME_Calendar = self.driver.find_element(By.XPATH, '//*[@id="toplevel_page_mec-intro"]/a/div[3]')
        ME_Calendar.click()
        time.sleep(2.5)
        add_event_menu_button = self.driver.find_element(By.XPATH, '//*[@id="toplevel_page_mec-intro"]/ul/li[4]/a')
        add_event_menu_button.click()
        time.sleep(2.5)
        self.driver.quit()


if __name__ == "__main__":
    wp = CEIWordPress()
    wp.post_events()
