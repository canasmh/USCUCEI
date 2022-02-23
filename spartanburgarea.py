from driver import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import datetime


class SpartanburgArea(Driver):

    def __init__(self):
        super().__init__()
        self.url = "http://spartanburgareasc.chambermaster.com/events/"
        self.events = []

    @staticmethod
    def format_date(date):

        month_conversion = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
        }

        month, day, year = date.split(" ")
        month = month_conversion[month]
        day = int(day[:-1])
        year = int(year)

        new_date = datetime.date(year, month, day)

        return new_date.strftime("%B %d, %Y")

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

            try:
                link = self.driver.find_element(By.CSS_SELECTOR, "div.gz-event-website a").get_attribute("href")
            except NoSuchElementException:
                back_button = self.driver.find_element(By.CSS_SELECTOR, "div.gz-page-return a")
                self.driver.get(back_button.get_attribute("href"))
                continue

            # Date and time of event
            event_dt = self.driver.find_elements(By.CSS_SELECTOR, "div.gz-event-date span")
            date = self.format_date(' '.join(event_dt[0].text.split(" ")[1:]))
            time = self.format_time(event_dt[1].text)
            title = self.driver.find_element(By.CSS_SELECTOR, "h1.gz-pagetitle").text


            description_list = self.driver.find_elements(By.CSS_SELECTOR, "div.col p")

            description = ""
            for item in description_list:
                description += item.text

            event_dict = {
                "Title": title,
                "Date": date,
                "Time": time,
                "Link": link,
                "Description": description
            }

            self.events.append(event_dict)

            # Go back to calendar page.
            back_button = self.driver.find_element(By.CSS_SELECTOR, "div.gz-page-return a")
            self.driver.get(back_button.get_attribute("href"))
        self.driver.quit()


if __name__ == "__main__":
    sa = SpartanburgArea()
    sa.get_events()
