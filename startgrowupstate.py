import datetime

from driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import date
import sys
import time


def format_date(event_date):
    """Convert date from string to datetime object"""

    convert_month = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }

    event_date = datetime.date(int(event_date[-4:]), convert_month[event_date[0:3]], int(event_date[4:6]))

    return event_date.strftime("%B %d, %Y")


class StartGrowUpstate(Driver):
    """Class in charged of scraping the StartGrowUpstate Event calendar"""

    def __init__(self, n_scrolls=200):
        super().__init__()
        self.url = "https://www.startgrowupstate.com/events"
        self.name = "Start Grow Upstate"
        self.events = []
        self.n_scrolls = n_scrolls

    def load_lazy(self):
        html_body = self.driver.find_element(By.TAG_NAME, "body")
        for _ in range(self.n_scrolls):
            html_body.send_keys(Keys.PAGE_DOWN)

    def get_events(self):
        """Method in charge of scraping the events."""
        self.driver.get(self.url)

        # GET THE NUMBER OF EVENTS
        time.sleep(5)
        n_events_div = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[1]/h3/div")
        n_events = int(n_events_div.text.split(" ")[0])
        print(f"Number of events: {n_events}")

        i = 1
        while i <= n_events:
            self.load_lazy()

            """
            COMMENT: This page is very verrryyy interesting. Theres a total of like 10 classes used through out the whole thing
            and there aren't very many unique edintifiers for the elements I need access to...

            So I'm getting the calendar_container using XPATH, and then getting calendar items, children of calendar_container.

            The problem is, that the XPath to the container... changes ? 🤔 so thats what the following try block checks..
            
            """
            try:
                calendar_container = self.driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div[3]")
                calendar_item = calendar_container.find_elements(By.CLASS_NAME, f"GroupItem")[i - 1]
            except (IndexError, NoSuchElementException):
                calendar_container = self.driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[3]")
                calendar_item = calendar_container.find_elements(By.CLASS_NAME, f"GroupItem")[i - 1]
            link_to_event_page = calendar_item.find_element(By.TAG_NAME, "a")
            link = link_to_event_page.get_attribute("href")
            self.driver.get(link)
            self.driver.switch_to.window(self.driver.window_handles[0])
            print("Second window title = " + self.driver.title)
            back_button = self.driver.find_element(By.LINK_TEXT, "Back to the Events Directory")
            back_button.click()
            self.driver.switch_to.window(self.driver.window_handles[0])
            print("Second window title = " + self.driver.title)
            i += 1
            print("i: ", i)

        sys.exit()

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
