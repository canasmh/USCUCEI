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
            title = event[0].upper()
            date = event[1]
            event_time = event[2]
            link = event[3]
            description = event[4]
            posted = event[5]

            title_input = self.driver.find_element(By.XPATH, '//*[@id="title"]')
            title_input.send_keys(title.capitalize())

            for i in range(len(title)):
                title_input.send_keys(Keys.BACKSPACE)

            # Enter description
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '//*[@id="content_ifr"]'))
            text_area = self.driver.find_element(By.XPATH, '//*[@id="tinymce"]')
            text_area.click()
            text_area.send_keys(description)
            time.sleep(0.5)
            for i in range(len(description)):
                text_area.send_keys(Keys.BACKSPACE)
            self.driver.switch_to.parent_frame()
            start_date_button = self.driver.find_element(By.XPATH, '//*[@id="mec_start_date"]')
            start_date_button.click()
            start_month_picker = self.driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[1]')
            start_month_picker.click()
            start_month_options = self.driver.find_elements(By.CSS_SELECTOR, "select.ui-datepicker-month option")

            for month in start_month_options:
                if month.text == date[0:3]:
                    month.click()
                    time.sleep(1.5)
                    break

            start_time_button = self.driver.find_elements(By.CSS_SELECTOR, "#mec_start_hour option")

            time.sleep(0.5)
            print(event)
        self.driver.quit()


if __name__ == "__main__":
    wp = CEIWordPress()
    wp.post_events()
