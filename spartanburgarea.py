from driver import Driver
from selenium.webdriver.common.by import By


class SpartanburgArea(Driver):

    def __init__(self):
        super().__init__()
        self.url = "http://spartanburgareasc.chambermaster.com/events/"

    def get_events(self):
        self.driver.get(self.url)

        events = self.driver.find_elements(By.CSS_SELECTOR, "a span.gz-img-placeholder")

        for event in events:
            print(event.click())
        self.driver.quit()


sa = SpartanburgArea()
sa.get_events()