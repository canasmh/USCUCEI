import datetime
from driver import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def convert_date_to_datetime(event_date):
    month_conversion = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    month, day, year = event_date.split(' ')
    month = int(month_conversion[month])
    day = int(day[:-1])
    year = int(year)

    return datetime.datetime(year, month, day)


class GreenvilleChamber(Driver):

    def __init__(self):
        super().__init__()
        self.url = "https://www.greenvillechamber.org/index.php?src=events&srctype=glance&submenu=_newsevents"
        self.events = []

    def go_to_next_month(self):
        next_button = self.driver.find_element(By.CSS_SELECTOR, "a span.fa-chevron-circle-right")
        next_button.click()

    def get_calendar_data(self):
        calendar = self.driver.find_elements(By.CSS_SELECTOR, "td.eventOn")
        return calendar

    def go_back(self):
        go_back_button = self.driver.find_element(By.LINK_TEXT, "Go Back")
        go_back_button.click()

    def get_event_info(self, event_link):

        try:
            event_title = self.driver.find_element(By.CSS_SELECTOR, "h1.pagetitle").text
        except NoSuchElementException:
            event_title = "N/A"

        try:
            event_date = self.driver.find_element(By.CSS_SELECTOR, "div.date").text.split(": ")[-1]
        except NoSuchElementException:
            event_date = "N/A"

        try:
            event_time = self.driver.find_element(By.CSS_SELECTOR, "div.time").text.split(": ")[-1]
        except NoSuchElementException:
            event_time = "N/A"

        try:
            event_description = self.driver.find_element(By.CSS_SELECTOR, "div.description").text
        except NoSuchElementException:
            event_description = "N/A"

        # event_location = self.driver.find_element_by_css_selector("div.address").text

        event_dict = {
            "Title": event_title,
            "Date": event_date,
            "Time": event_time,
            "Link": event_link,
            "Description": event_description
        }

        return event_dict

    def get_events(self):
        self.driver.get(self.url)

        month = 0
        max_month = 3

        while month < max_month:
            day = 0
            n_days = len(self.get_calendar_data())

            while day < n_days - 1:
                # This is a nested list. Each item in list is a day.
                events_per_day = self.get_calendar_data()

                # These are the events on the 'nth' day.
                events = events_per_day[day].find_elements(By.CSS_SELECTOR, "a")

                if len(events) == 0:
                    day += 1
                    continue
                else:
                    for i in range(len(events)):
                        event_link = events[i].get_property("href")

                        events[i].click()
                        event_dict = self.get_event_info(event_link)

                        if convert_date_to_datetime(event_dict["Date"]) < datetime.datetime.today():
                            self.go_back()
                            events_per_day = self.get_calendar_data()
                            events = events_per_day[day].find_elements(By.CSS_SELECTOR, "a")
                            print("Event has already passed.")

                            continue

                        print(event_dict)
                        self.go_back()
                        self.events.append(event_dict)
                        events_per_day = self.get_calendar_data()
                        events = events_per_day[day].find_elements(By.CSS_SELECTOR, "a")
                    day += 1

            next_month = self.driver.find_element(By.XPATH, "//*[@id='calendarDetail']/table/tbody/tr[1]/td[3]/a")
            self.driver.execute_script("arguments[0].click();", next_month)
            month += 1

        self.driver.quit()
