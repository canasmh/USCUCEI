from driver import Driver
from selenium.webdriver.common.by import By


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

    def get_events(self):
        self.driver.get(self.url)

        self.driver.quit()
