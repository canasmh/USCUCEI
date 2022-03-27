from driver import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import datetime


class SpartanburgArea(Driver):
    """This class is in charge of scraping the Spartanburg Area Chamber of Commerce event page"""

    def __init__(self):
        super().__init__()
        self.url = "http://spartanburgareasc.chambermaster.com/events/"
        self.name = "Spartanburg Area"
        self.events = []

    @staticmethod
    def format_date(date):
        """This method is to format a string from Mon day, year to Month day, Year"""

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
        """This method removes unecessary string from time"""

        new_time = time.split(" ")[:-1]

        return " ".join(new_time)

    def get_events(self):
        """This method is the main method used to scrape the events."""

        self.driver.get(self.url)

        # Get all of the events
        n_events = len(self.driver.find_elements(
            By.CSS_SELECTOR, ".card-header a"))

        # Loop through events
        for n in range(0, n_events):
            # Go to event page.
            event = self.driver.find_elements(
                By.CSS_SELECTOR, ".card-header a")[n]
            self.driver.get(event.get_attribute("href"))

            # Get event link
            try:
                link = self.driver.find_element(
                    By.CSS_SELECTOR, "div.gz-event-website a").get_attribute("href")
            # If there is no link, move on to next event.
            except NoSuchElementException:
                back_button = self.driver.find_element(
                    By.CSS_SELECTOR, "div.gz-page-return a")
                self.driver.get(back_button.get_attribute("href"))
                continue

            # Date and time of event
            event_dt = self.driver.find_elements(
                By.CSS_SELECTOR, "div.gz-event-date span")
            date = self.format_date(' '.join(event_dt[0].text.split(" ")[1:]))
            time = self.format_time(event_dt[1].text)
            # Get title of event
            title = self.driver.find_element(
                By.CSS_SELECTOR, "h1.gz-pagetitle").text

            description_list = self.driver.find_elements(
                By.CSS_SELECTOR, "div.col")

            # Get event description
            description = ""
            for item in description_list:
                description += item.text

                if len(description) == 0:
                    continue
                else:
                    description += "\n"

            description = description.replace(title + "\n", "")

            # Create event dictionary
            event_dict = {
                "Title": title,
                "Date": date,
                "Time": time,
                "Link": link,
                "Description": description
            }

            print(event_dict)
            self.events.append(event_dict)

            # Go back to calendar page.
            back_button = self.driver.find_element(
                By.CSS_SELECTOR, "div.gz-page-return a")
            self.driver.get(back_button.get_attribute("href"))
        self.driver.quit()


if __name__ == "__main__":
    sa = SpartanburgArea()
    sa.get_events()
