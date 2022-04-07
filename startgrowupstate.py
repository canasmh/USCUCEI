import datetime

from driver import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import date


def format_date(event_date):
    """Convert date from string to datetime object"""

    month, day, year = event_date.split("/")
    event_date = datetime.date(int(year), int(month), int(day))

    return event_date


class StartGrowUpstate(Driver):
    """Class in charged of scraping the StartGrowUpstate Event calendar"""

    def __init__(self):
        super().__init__()
        self.url = "https://www.startgrowupstate.com/explore-events"
        self.name = "Start Grow Upstate"
        self.events = []

    def get_events(self):
        """Method in charge of scraping the events."""
        self.driver.get(self.url)
        calendar_object = self.driver.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(calendar_object)

        # Make sure you're scraping today's calendar
        today_btn = self.driver.find_element(By.XPATH, '//*[@id="calendarView"]/div/div/div[1]/div[2]/div[1]')
        today_btn.click()

        n = 0
        # Get all of the events
        events = self.driver.find_elements(By.CSS_SELECTOR, ".calendarRecord")

        # Get the total number events
        n_events = len(events)
        # Got to event page
        events[n].click()
        while n < n_events:
            # Get event title
            title = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div'
            ).text

            # Get event date
            event_date = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div/div[1]/div'
            ).text

            event_date = format_date(event_date)

            # Check if event has already passed
            if event_date < date.today():
                n += 1
                next_event_button = self.driver.find_element(
                    By.XPATH,
                    '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[1]/div/div/div/div[1]/div[3]'
                )
                next_event_button.click()
                continue

            # Get event description
            description = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[7]/div[2]/div/div/div/div/div[1]'
            ).text

            # Get event start time
            start_time = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div'
            ).text

            # Get event end time (if any)
            try:
                end_time = self.driver.find_element(
                    By.XPATH,
                    '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div'
                ).text
            except NoSuchElementException:
                end_time = "Not Specified"

            # Get event link
            link_button = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[5]/div[2]/div/div/div/a'
            )

            link = link_button.get_attribute("href")

            event_dict = {
                "Title": title,
                "Date": event_date.strftime("%B %d, %Y"),
                "Time": start_time + " - " + end_time,
                "Link": link,
                "Description": description
            }

            print(event_dict)
            self.events.append(event_dict)

            # Go to next event.
            next_event_button = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[1]/div/div/div/div[1]/div[3]'
            )
            next_event_button.click()
            n += 1

        self.driver.quit()


if __name__ == "__main__":
    sgu = StartGrowUpstate()
    sgu.get_events()
