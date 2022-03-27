import datetime
from driver import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def convert_date(event_date):
    """This function converts a date from a string to a datetime object"""
    error = False
    event_date = event_date.replace(",", "")
    month_conversion = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    try:
        month, day, year = event_date.split(' ')
    except Exception as err:
        print(f"Error converting date:\n{err}")
        print(f"Original Date: {event_date}")
        if "-" in event_date:
            start_of_date, other_day = event_date.split("-")
            end_of_date = other_day.split(' ')[-1]
            event_date = start_of_date + end_of_date
            print(f"Formatted Date: {event_date}")
            error = True

    if error:
        try:
            month, day, year = event_date.split(' ')
        except Exception as err:
            print(f"Error was unresolved: {err}")
        else:
            print("Error was resolved")

    month = int(month_conversion[month])
    day = int(day)
    year = int(year)

    return datetime.date(year, month, day)


def format_date(date):
    """This function converts a date thats formatted as MM/DD/YYYY to Month Day, Year"""
    date = convert_date(date)

    return date.strftime("%B %d, %Y")


class GreenvilleChamber(Driver):
    """ This class is in charge of scraping the Greenville Chambers of Commerce events page"""

    def __init__(self):
        super().__init__()
        self.url = "https://www.greenvillechamber.org/index.php?src=events&srctype=glance&submenu=_newsevents"
        self.name = "Greenville Chambers"
        self.events = []

    def get_calendar_data(self):
        """This function gets all of the items displayed on the calendar"""
        calendar = self.driver.find_elements(By.CSS_SELECTOR, "td.eventOn")
        return calendar

    def go_back(self):
        """This function goes from the event page back to the calendar page"""
        go_back_button = self.driver.find_element(By.LINK_TEXT, "Go Back")
        go_back_button.click()

    def get_event_info(self, event_link):
        """This function is in charge of getting the event title, date, time and description. Returns a dictionary with
        title, date, time, link and description as keys."""

        try:
            event_title = self.driver.find_element(
                By.CSS_SELECTOR, "h1.pagetitle").text
        except NoSuchElementException or Exception as err:
            event_title = "N/A"

        try:
            event_date = self.driver.find_element(By.CSS_SELECTOR, "div.date").text.split(": ")[-1]
            event_date = format_date(event_date)
        except NoSuchElementException or Exception as err:
            event_date = "N/A"

        try:
            event_time = self.driver.find_element(
                By.CSS_SELECTOR, "div.time").text.split(": ")[-1]
        except NoSuchElementException or Exception as err:
            event_time = "N/A"

        try:
            event_description = self.driver.find_element(
                By.CSS_SELECTOR, "div.description").text
        except NoSuchElementException or Exception as err:
            event_description = "N/A"

        # event_location = self.driver.find_element_by_css_selector("div.address").text

        event_dict = {
            "Title": event_title,
            "Date": event_date,
            "Time": event_time,
            "Link": event_link,
            "Description": event_description
        }

        print(event_dict)

        return event_dict

    def get_events(self):
        """Main function used to scrape events."""
        self.driver.get(self.url)

        # Scrape the following three months
        month = 0
        max_month = 3

        while month < max_month:
            # Get the number of events for the month.
            day = 0
            n_days = len(self.get_calendar_data())

            while day < n_days - 1:
                # Get all of the events in the month.
                events_per_day = self.get_calendar_data()

                # Get all of the events on day 'day'.
                events = events_per_day[day].find_elements(
                    By.CSS_SELECTOR, "a")

                # If there are not any events in the day, move on.
                if len(events) == 0:
                    day += 1
                    continue
                else:
                    for i in range(len(events)):
                        # Get event link and go to event page
                        event_link = events[i].get_property("href")
                        events[i].click()

                        # Make the event dictionary
                        event_dict = self.get_event_info(event_link)

                        # Check if the event has passed
                        if datetime.datetime.strptime(event_dict['Date'], "%B %d, %Y") < datetime.datetime.today():
                            self.go_back()
                            events_per_day = self.get_calendar_data()
                            events = events_per_day[day].find_elements(
                                By.CSS_SELECTOR, "a")
                            # If so, move on
                            continue

                        # Go back to main page and append dictionary to events attribute.
                        self.go_back()
                        self.events.append(event_dict)
                        events_per_day = self.get_calendar_data()
                        events = events_per_day[day].find_elements(
                            By.CSS_SELECTOR, "a")
                    day += 1

            # Go to the next month.
            next_month = self.driver.find_element(
                By.XPATH, "//*[@id='calendarDetail']/table/tbody/tr[1]/td[3]/a")
            self.driver.execute_script("arguments[0].click();", next_month)
            month += 1

        self.driver.quit()


if __name__ == "__main__":
    gc = GreenvilleChamber()
    gc.get_events()
