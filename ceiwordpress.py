from driver import Driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import sqlite3
import os
import time

# Load environment variables
load_dotenv()


class CEIWordPress(Driver):
    """This class is in charged of uploading all of the events from the database to USCUCEI"""
    def __init__(self):
        super().__init__()
        self.url = os.environ.get("WP_URL")
        self.db_name = '/Users/manny/Documents/Freelancing/USCUCEI/events.db'
        self.table_name = 'events'
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.events_not_posted = []

    def login(self):
        """This method logs in to the WordPress page as an admin"""
        username_field = self.driver.find_element(By.ID, "user_login")
        username_field.send_keys(os.environ.get("WP_USERNAME"))
        password_field = self.driver.find_element(By.ID, "user_pass")
        password_field.send_keys(os.environ.get("WP_PASSWORD"))
        self.driver.find_element(By.ID, "wp-submit").click()

    def go_to_add_event_page(self):
        """This method is used to the 'Add Event' page on WordPress"""
        self.driver.get(os.environ.get("WP_ADD_POST"))

    def add_title(self, title):
        """This method inserts the title of the event"""
        title_input = self.driver.find_element(By.XPATH, '//*[@id="title"]')
        title_input.send_keys(title)

    def add_description(self, description, link):
        """This method inserts the description of event as well as the event link"""
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
        """This method selects the correct start date of the event"""
        start_date_button = self.driver.find_element(By.XPATH, '//*[@id="mec_start_date"]')
        start_date_button.click()
        start_month_picker = self.driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[1]')
        start_month_picker.click()
        start_month_options = self.driver.find_elements(By.CSS_SELECTOR, "select.ui-datepicker-month option")

        # Loop through all the months until the correct one is select
        for month in start_month_options:
            if month.text == date[0:3]:
                month.click()
                break
        day_options = self.driver.find_elements(By.CSS_SELECTOR, "td[data-handler='selectDay']")

        # Loop through all the days in the month until the correct day is selected
        for day in day_options:
            event_day = date.split(' ')[1]
            if day.text == event_day[0:len(event_day) - 1]:
                day.click()

    def add_end_date(self, date):
        """This method selects the correct end date for the event"""
        end_date_button = self.driver.find_element(By.XPATH, '//*[@id="mec_end_date"]')
        end_date_button.click()
        end_month_picker = self.driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[1]')
        end_month_picker.click()
        end_month_options = self.driver.find_elements(By.CSS_SELECTOR, "select.ui-datepicker-month option")

        # Loop through all the months until the correct one is select
        for month in end_month_options:
            if month.text == date[0:3]:
                month.click()
                break

        day_options = self.driver.find_elements(By.CSS_SELECTOR, "td[data-handler='selectDay']")
        # Loop through all the days in the month until the correct day is selected
        for day in day_options:
            event_day = date.split(' ')[1]
            if day.text == event_day[0:len(event_day) - 1]:
                day.click()

    def add_start_time(self, event_time):
        """This method selects the correct start time of the event (if any)."""
        if event_time == "N/A":
            self.driver.find_element(By.XPATH, '// *[ @ id = "mec_hide_time"]').click()
        else:
            # Options for the hour -- from 1 - 12
            start_time_hr_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_start_hour option")

            # Loop through all the hour options until you find the correct hour
            for start_time in start_time_hr_options:
                start, end = event_time.split(' - ')

                # if the hour matches the time in the database, click on that one.
                if start_time.text == start.split(':')[0]:
                    start_time.click()
                    break

            start_time_min_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_start_minutes option")

            # Loop through all the minute options until you find the correct minute
            for start_time in start_time_min_options:
                start, end = event_time.split(' - ')
                min = start.split(':')[1]

                if start_time.text == min[0:2]:
                    start_time.click()
                    break

            start_time_ampm_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_start_ampm option")

            # Select either AM or PM
            for ampm in start_time_ampm_options:
                start, end = event_time.split(' - ')
                min = start.split(':')[1]

                if str(ampm.text).lower() == min[len(min) - 2: len(min)].lower():
                    ampm.click()
                    break

    def add_end_time(self, event_time):
        """This method selects the correct start time of the event (if any)."""
        end_time_hr_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_end_hour option")

        if event_time == "N/A":
            hide_time_button = self.driver.find_element(By.XPATH, '//*[@id="mec_hide_time"]')
            hide_time_button.click()
        # Make sure end time is specified
        elif event_time.split(' - ')[1] == 'Not Specified':
            # Hide Event Time
            self.driver.find_element(By. XPATH, '//*[@id="mec_hide_end_time"]').click()

        else:
            # Select the right hour for the end time
            for end_time in end_time_hr_options:
                start, end = event_time.split(' - ')

                if end_time.text == end.split(':')[0]:
                    end_time.click()
                    break

            start_time_min_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_end_minutes option")

            # Select the right minute for the end time
            for end_time in start_time_min_options:
                start, end = event_time.split(' - ')
                min = end.split(':')[1]

                if end_time.text == min[0:2]:
                    end_time.click()
                    break

            start_time_ampm_options = self.driver.find_elements(By.CSS_SELECTOR, "#mec_end_ampm option")

            # Select whether you're in am or pm
            for ampm in start_time_ampm_options:
                start, end = event_time.split(' - ')
                min = end.split(':')[1]

                if str(ampm.text).lower() == min[len(min) - 2: len(min)].lower():
                    ampm.click()
                    break

    def post_events(self):
        """Main method in charge of posting the events to WordPress"""
        self.driver.get(self.url)
        self.login()
        self.go_to_add_event_page()

        # ID's of successfully posted events will be appended to this list
        ids_of_posted_events = []

        # Select the events from the database
        events = self.cursor.execute(f"SELECT * FROM {self.table_name}")

        # Loop through the events
        for event in events:
            title = event[0]
            date = event[1]
            event_time = event[2]
            link = event[3]
            description = event[4]
            posted = event[5]
            id = event[6]

            # Replace special characters made in eventdb.py
            title = title.replace("&&&", "'")
            description = description.replace("&&&", "'")
            if "&&n" in description:
                description = description.split("&&n")

            if not posted:
                # Try posting an event
                self.add_title(title.upper())
                self.add_description(description, link)
                self.add_start_date(date)
                self.add_start_time(event_time)
                self.add_end_date(date)
                self.add_end_time(event_time)
                try:
                    publish_button = self.driver.find_element(By.XPATH, '//*[@id="publish"]')
                    self.driver.execute_script("arguments[0].click();", publish_button)

                except Exception as err:
                    # If there is an error, append event to a list as a dictionary. Quit the broswer, login to WP and
                    # move on to next event.
                    print(f"Event not posted: {title.upper()}\n {err}")
                    self.events_not_posted.append({
                        "title": title,
                        "date": date,
                        "time": event_time
                    })
                    # restart the driver
                    self.driver.quit()
                    self.driver = webdriver.Chrome(service=self.service)
                    self.driver.get(os.environ.get("WP_URL"))
                    self.login()
                    self.go_to_add_event_page()

                else:
                    # If successful, append id to to list and move return to add new event page
                    print(f"Event Published: {title}")
                    ids_of_posted_events.append(id)
                    time.sleep(3)
                    self.go_to_add_event_page()

            else:
                continue

        # Check if any events were posted
        if len(ids_of_posted_events) != 0:
            # If so, loop through posted events and change the Posted boolean to 1
            for id in ids_of_posted_events:
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
