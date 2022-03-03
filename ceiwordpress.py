from driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import sqlite3
import os
import time


# TODO: CHANGE THE POSTED ELEMENT IN DB TO FALSE (ONCE UPLOADED).
# TODO: Upload event link as a hypertext in the description.
# TODO: Post events and refresh the 'add-event' page.
# Add

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

    def add_title(self, title):
        title_input = self.driver.find_element(By.XPATH, '//*[@id="title"]')
        title_input.send_keys(title.capitalize())

    def add_description(self, description):
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '//*[@id="content_ifr"]'))
        text_area = self.driver.find_element(By.XPATH, '//*[@id="tinymce"]')
        text_area.click()
        text_area.send_keys(description)
        self.driver.switch_to.parent_frame()

    def add_start_date(self, date):
        start_date_button = self.driver.find_element(By.XPATH, '//*[@id="mec_start_date"]')
        start_date_button.click()
        # start_month_picker = self.driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[1]')
        # start_month_picker.click()
        start_month_options = self.driver.find_elements(By.CSS_SELECTOR, "select.ui-datepicker-month option")

        for month in start_month_options:
            if month.text == date[0:3]:
                month.click()
                time.sleep(1.5)
                break
        day_options = self.driver.find_elements(By.CSS_SELECTOR, "td[data-handler='selectDay']")

        for day in day_options:
            event_day = date.split(' ')[1]
            if day.text == event_day[0:len(event_day) - 1]:
                day.click()
                
    def add_end_date(self, date):
        end_date_button = self.driver.find_element(By.XPATH, '//*[@id="mec_end_date"]')
        end_date_button.click()
        # end_month_picker = self.driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[1]')
        # end_month_picker.click()
        end_month_options = self.driver.find_elements(By.CSS_SELECTOR, "select.ui-datepicker-month option")

        for month in end_month_options:
            if month.text == date[0:3]:
                month.click()
                time.sleep(1.5)
                break
        day_options = self.driver.find_elements(By.CSS_SELECTOR, "td[data-handler='selectDay']")

        for day in day_options:
            event_day = date.split(' ')[1]
            if day.text == event_day[0:len(event_day) - 1]:
                day.click()

    def add_start_time(self, event_time):
        start_time_hr_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_start_hour option")

        for start_time in start_time_hr_options:
            start, end = event_time.split(' - ')

            if start_time.text == start.split(':')[0]:
                start_time.click()
                break

        start_time_min_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_start_minutes option")

        for start_time in start_time_min_options:
            start, end = event_time.split(' - ')
            min = start.split(':')[1]

            if start_time.text == min[0:2]:
                start_time.click()
                break

        start_time_ampm_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_start_ampm option")

        for ampm in start_time_ampm_options:
            start, end = event_time.split(' - ')
            min = start.split(':')[1]

            if ampm.text == min[len(min) - 2: len(min)]:
                ampm.click()
                break

    def add_end_time(self, event_time):
        end_time_hr_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_end_hour option")

        if event_time.split(' - ')[1] == 'Not Specified':
            print("No Event Time specified")
        else:
            for end_time in end_time_hr_options:
                start, end = event_time.split(' - ')

                if end_time.text == start.split(':')[0]:
                    end_time.click()
                    break

            start_time_min_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_end_minutes option")

            for end_time in start_time_min_options:
                start, end = event_time.split(' - ')
                min = start.split(':')[1]

                if end_time.text == min[0:2]:
                    end_time.click()
                    break

            start_time_ampm_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_end_ampm option")

            for ampm in start_time_ampm_options:
                start, end = event_time.split(' - ')
                min = start.split(':')[1]

                if ampm.text == min[len(min) - 2: len(min)]:
                    ampm.click()
                    break



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

            if posted == 'False':
                self.add_title(title)
                self.add_description(description)
                self.add_start_date(date)
                self.add_start_time(event_time)
                self.add_end_date(date)
                self.add_end_time(event_time)

            else:
                continue

            time.sleep(0.5)
            print(event)
        self.driver.quit()


if __name__ == "__main__":
    wp = CEIWordPress()
    wp.post_events()
