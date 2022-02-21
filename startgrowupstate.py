from driver import Driver
from selenium.webdriver.common.by import By


class StartGrowUpstate(Driver):

    def __init__(self):
        super().__init__()
        self.url = "https://www.startgrowupstate.com/explore-events"
        self.events = []

    def get_events(self):
        self.driver.get(self.url)
        calendar_object = self.driver.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(calendar_object)
        events = self.driver.find_elements(By.CSS_SELECTOR, ".calendarRecord")
