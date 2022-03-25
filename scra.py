from driver import Driver
from selenium.webdriver.common.by import By
import datetime


def convert_to_date_time(date):
    """Converts string to datetime object"""
    year, month, day = date.split('-')

    return datetime.date(int(year), int(month), int(day))


class SouthCarolinaResearchAuthority(Driver):
    """Object in charge of scraping the South Carolina Research Authority."""

    def __init__(self):
        super().__init__()
        self.url = "https://www.scra.org/calendar/list/"
        self.name = "SCRA"
        self.events = []

    def get_events(self):
        """Method in charge of scraping event data"""
        self.driver.get(self.url)

        # Get all of the events listed on the page
        events = self.driver.find_elements(
            By.CSS_SELECTOR, "div.tribe-events-calendar-list__event-details")

        # Loop through events
        for i in range(len(events)):
            events = self.driver.find_elements(
                By.CSS_SELECTOR, "div.tribe-events-calendar-list__event-details")
            datetime_element = events[i].find_element(By.CSS_SELECTOR, "time")
            # Get event date
            date = convert_to_date_time(
                datetime_element.get_attribute("datetime"))

            # Make sure event hasn't already passed.
            if date < datetime.date.today():
                continue

            # Get event time
            time = str(datetime_element.text).split('@ ')[-1]

            # Get event link
            link_element = events[i].find_element(
                By.CSS_SELECTOR, "a.tribe-events-calendar-list__event-title-link")
            # Get event Text
            title = link_element.text
            link = link_element.get_attribute("href")
            link_element.click()

            new_window = self.driver.window_handles[-1]
            self.driver.switch_to.window(new_window)

            # Get event Description (if any)
            event_details = self.driver.find_element(
                By.CSS_SELECTOR, "div.tribe-events-single-event-description")
            p_elements = event_details.find_elements(By.CSS_SELECTOR, "p")
            description = "N/A"

            for p_element in p_elements:
                if len(p_element.text) < 100:
                    continue
                else:
                    description = p_element.text
                    break

            # Create event dictionary
            event_dict = {
                "Title": title,
                "Date": date.strftime("%B %d, %Y"),
                "Time": time,
                "Link": link,
                "Description": description
            }

            print(event_dict)
            self.events.append(event_dict)

        self.driver.quit()


if __name__ == "__main__":
    scra = SouthCarolinaResearchAuthority()
    scra.get_events()
