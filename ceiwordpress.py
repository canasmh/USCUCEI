from driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import sqlite3
import os
import time

# TODO: Debug -- there was an error uploading events to wordpress (maybe because sometimes are N/A)

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
        ME_Calendar = self.driver.find_element(By.XPATH, '//*[@id="toplevel_page_mec-intro"]/a/div[3]')
        ME_Calendar.click()

        add_event_menu_button = self.driver.find_element(By.XPATH, '//*[@id="toplevel_page_mec-intro"]/ul/li[4]/a')
        add_event_menu_button.click()

    def add_title(self, title):
        title_input = self.driver.find_element(By.XPATH, '//*[@id="title"]')
        title_input.send_keys(title)

    def add_description(self, description, link):
        switch_to_text = self.driver.find_element(By.XPATH, '//*[@id="content-html"]')
        switch_to_text.click()
        text_area = self.driver.find_element(By.XPATH, '//*[@id="content"]')
        text_area.click()
        if type(description) is list:
            for item in description:
                text_area.send_keys(item)
                text_area.send_keys(Keys.RETURN)
                text_area.send_keys(Keys.RETURN)
        else:
            text_area.send_keys(description)

        if link != "N/A":
            text_area.send_keys(f"\n<a href={link}>Click HERE to register</a>")

    def add_start_date(self, date):
        start_date_button = self.driver.find_element(By.XPATH, '//*[@id="mec_start_date"]')
        start_date_button.click()
        start_month_picker = self.driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[1]')
        start_month_picker.click()
        start_month_options = self.driver.find_elements(By.CSS_SELECTOR, "select.ui-datepicker-month option")

        for month in start_month_options:
            if month.text == date[0:3]:
                month.click()
                break
        day_options = self.driver.find_elements(By.CSS_SELECTOR, "td[data-handler='selectDay']")

        for day in day_options:
            event_day = date.split(' ')[1]
            if day.text == event_day[0:len(event_day) - 1]:
                day.click()
                
    def add_end_date(self, date):
        end_date_button = self.driver.find_element(By.XPATH, '//*[@id="mec_end_date"]')
        end_date_button.click()
        end_month_picker = self.driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[1]')
        end_month_picker.click()
        end_month_options = self.driver.find_elements(By.CSS_SELECTOR, "select.ui-datepicker-month option")

        for month in end_month_options:
            if month.text == date[0:3]:
                month.click()

                break
        day_options = self.driver.find_elements(By.CSS_SELECTOR, "td[data-handler='selectDay']")

        for day in day_options:
            event_day = date.split(' ')[1]
            if day.text == event_day[0:len(event_day) - 1]:
                day.click()

    def add_start_time(self, event_time):

        if event_time == "N/A":
            self.driver.find_element(By.XPATH, '// *[ @ id = "mec_hide_time"]').click()
        else:
            # Options for the hour -- from 1 - 12
            start_time_hr_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_start_hour option")

            for start_time in start_time_hr_options:
                start, end = event_time.split(' - ')

                # if the hour matches the time in the database, click on that one.
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

                if str(ampm.text).lower() == min[len(min) - 2: len(min)].lower():
                    ampm.click()
                    break

    def add_end_time(self, event_time):
        end_time_hr_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_end_hour option")

        if event_time == "N/A":
            pass

        elif event_time.split(' - ')[1] == 'Not Specified':
            # Hide Event Time
            self.driver.find_element(By. XPATH, '//*[@id="mec_hide_end_time"]').click()
            print("No Event Time specified")
        else:
            for end_time in end_time_hr_options:
                start, end = event_time.split(' - ')

                if end_time.text == end.split(':')[0]:
                    end_time.click()
                    break

            start_time_min_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_end_minutes option")

            for end_time in start_time_min_options:
                start, end = event_time.split(' - ')
                min = end.split(':')[1]

                if end_time.text == min[0:2]:
                    end_time.click()
                    break

            start_time_ampm_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_end_ampm option")

            for ampm in start_time_ampm_options:
                start, end = event_time.split(' - ')
                min = end.split(':')[1]

                if str(ampm.text).lower() == min[len(min) - 2: len(min)].lower():
                    ampm.click()
                    break

    def post_events(self):
        self.driver.get(self.url)
        self.login()
        self.add_event_page()

        ids_to_be_posted = []
        events = self.cursor.execute(f"SELECT * FROM {self.table_name}")
        for event in events:
            title = event[0]
            date = event[1]
            event_time = event[2]
            link = event[3]
            description = event[4]
            posted = event[5]
            id = event[6]

            # Replace special characters made in eventdb.py
            description = description.replace("&&&", "'")
            if "&&n" in description:
                description = description.split("&&n")

            if not posted:
                try:
                    self.add_title("TEST " + title.upper())
                    self.add_description(description, link)
                    self.add_start_date(date)
                    self.add_start_time(event_time)
                    self.add_end_date(date)
                    self.add_end_time(event_time)
                    publish_button = self.driver.find_element(By.XPATH, '//*[@id="publish"]')
                    self.driver.execute_script("arguments[0].click();", publish_button)
                except Exception as err:
                    print(f"Event not posted:\nid: {id}\ntitle: {title.upper()}\n {err}")
                    self.driver.get("https://uscupstatecei.org/wp-admin/post-new.php?post_type=mec-events")
                    time.sleep(2)
                    self.driver.switch_to.alert.accept()
                else:
                    time.sleep(3)
                    self.driver.get("https://uscupstatecei.org/wp-admin/post-new.php?post_type=mec-events")
                    ids_to_be_posted.append(id)

            else:
                continue

        if len(ids_to_be_posted) != 0:
            for id in ids_to_be_posted:
                self.cursor.execute(f"UPDATE {self.table_name} SET Posted = '1' WHERE id = {id}")
                self.connection.commit()
                print(f"Record with id: {id} Updated Successfully.")
        else:
            print("No new events were posted...")

        self.connection.close()
        self.driver.quit()


if __name__ == "__main__":
    wp = CEIWordPress()
    wp.post_events()
