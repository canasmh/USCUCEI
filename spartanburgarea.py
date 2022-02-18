from driver import Driver
from selenium.webdriver.common.by import By

# TODO: Use href and driver.get instead of click method


class SpartanburgArea(Driver):

    def __init__(self):
        super().__init__()
        self.url = "http://spartanburgareasc.chambermaster.com/events/"

    @staticmethod
    def format_date(date):

        month_conversion = {
        "Jan": "January",
        "Feb": "February",
        "Mar": "March",
        "Apr": "April",
        "May": "May",
        "Jun": "June",
        "Jul": "July",
        "Aug": "August",
        "Sep": "September",
        "Oct": "October",
        "Nov": "November",
        "Dec": "December"
        }

        new_date = date.split(" ")

        new_date[0]= month_conversion[new_date[0]]

        return " ".join(new_date)

    @staticmethod
    def format_time(time):

        new_time = time.split(" ")[:-1]

        return " ".join(new_time)

    def get_events(self):

        self.driver.get(self.url)

        n_events = len(self.driver.find_elements(By.CSS_SELECTOR, ".card-header a"))

        for n in range(0, n_events):
            # Go to event page.
            event = self.driver.find_elements(By.CSS_SELECTOR, ".card-header a")[n]
            self.driver.get(event.get_attribute("href"))

            # Date and time of event
            event_dt = self.driver.find_elements(By.CSS_SELECTOR, "div.gz-event-date span")
            # format Weekday Month 01, YYYY
            date = self.format_date(' '.join(event_dt[0].text.split(" ")[1:]))
            time = self.format_time(event_dt[1].text)



            # Go back to calendar page.
            back_button = self.driver.find_element(By.CSS_SELECTOR, "div.gz-page-return a")
            self.driver.get(back_button.get_attribute("href"))
        self.driver.quit()


sa = SpartanburgArea()
sa.get_events()