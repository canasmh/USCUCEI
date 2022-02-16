from driver import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


class GreenvilleChamber(Driver):

    def __init__(self):
        super().__init__()
        self.url = "https://www.greenvillechamber.org/index.php?src=events&srctype=glance&submenu=_newsevents"
        self.events = []

    def go_to_next_month(self):
        next_button = self.driver.find_element(By.CSS_SELECTOR, "td.nextLink")
        next_button.click()

    def get_calendar_data(self):
        calendar = self.driver.find_elements(By.CSS_SELECTOR, "td.eventOn")
        return calendar

    def go_back(self):
        go_back_button = self.driver.find_element(By.LINK_TEXT, "Go Back")
        go_back_button.click()

    def get_events(self):
        self.driver.get(self.url)
        n = 0
        n_events = len(self.get_calendar_data())

        while n < n_events - 1:
            # This is a nested list. Each item in list is a day.
            calendar_data = self.get_calendar_data()

            # These are the events on the 'nth' day.
            events = calendar_data[n].find_elements(By.CSS_SELECTOR, "a")

            if len(events) == 0:
                n += 1
                continue
            else:
                for i in range(len(events)):
                    events[i].click()
                    self.go_back()
                    calendar_data = self.get_calendar_data()
                    events = calendar_data[n].find_elements(By.CSS_SELECTOR, "a")
                    i += 0

                n += 1

        self.driver.quit()
