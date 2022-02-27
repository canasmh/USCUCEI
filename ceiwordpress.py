from driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import sqlite3
import os
import time

load_dotenv()


class CEIWordPress(Driver):

    def __init__(self):
        super().__init__()
        self.url = os.environ.get("WP_URL")
        self.db_name = 'events.db'
        self.table_name = 'events'
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def login(self):
        username_field = self.driver.find_element(By.ID, "user_login")
        username_field.send_keys(os.environ.get("WP_USERNAME"))
        password_field = self.driver.find_element(By.ID, "user_pass")
        password_field.send_keys(os.environ.get("WP_PASSWORD"))
        self.driver.find_element(By.ID, "wp-submit").click()

    def add_event_page(self):
        time.sleep(2)
        ME_Calendar = self.driver.find_element(By.XPATH, '//*[@id="toplevel_page_mec-intro"]/a/div[3]')
        ME_Calendar.click()
        time.sleep(2)
        add_event_menu_button = self.driver.find_element(By.XPATH, '//*[@id="toplevel_page_mec-intro"]/ul/li[4]/a')
        add_event_menu_button.click()
        time.sleep(2)

    def post_events(self):
        self.driver.get(self.url)
        self.login()
        self.add_event_page()

        events = self.cursor.execute(f"SELECT * FROM {self.table_name}")
        for event in events:
            title_input = self.driver.find_element(By.XPATH, '//*[@id="title"]')
            title_input.send_keys(event[0])

            time.sleep(0.5)
            for i in range(500):
                title_input.send_keys(Keys.BACKSPACE)
            print(event)
            time.sleep(0.5)
        self.driver.quit()


if __name__ == "__main__":
    wp = CEIWordPress()
    wp.post_events()
