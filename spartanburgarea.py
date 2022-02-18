from driver import Driver
from selenium.webdriver.common.by import By

# TODO: Use href and driver.get instead of click method


class SpartanburgArea(Driver):

    def __init__(self):
        super().__init__()
        self.url = "http://spartanburgareasc.chambermaster.com/events/"

    def get_events(self):

        self.driver.get(self.url)

        n_events = len(self.driver.find_elements(By.CSS_SELECTOR, ".card-header a"))

        for n in range(0, n_events):
            # Go to event page.
            event = self.driver.find_elements(By.CSS_SELECTOR, ".card-header a")[n]
            self.driver.get(event.get_attribute("href"))

            # Go back to calendar page.
            back_button = self.driver.find_element(By.CSS_SELECTOR, "div.gz-page-return a")
            self.driver.get(back_button.get_attribute("href"))
        self.driver.quit()


sa = SpartanburgArea()
sa.get_events()