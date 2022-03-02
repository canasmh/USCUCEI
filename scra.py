from driver import Driver
from selenium.webdriver.common.by import By
import datetime


def convert_to_date_time(date):
    year, month, day = date.split('-')

    return datetime.date(int(year), int(month), int(day))


class SouthCarolinaResearchAuthority(Driver):

    def __init__(self):
        super().__init__()
        self.url = "https://www.scra.org/calendar/list/"
        self.events = []

    def get_events(self):

        self.driver.get(self.url)
        events = self.driver.find_elements(
            By.CSS_SELECTOR, "div.tribe-events-calendar-list__event-details")

        for i in range(len(events)):
            events = self.driver.find_elements(
                By.CSS_SELECTOR, "div.tribe-events-calendar-list__event-details")
            datetime_element = events[i].find_element(By.CSS_SELECTOR, "time")
            date = convert_to_date_time(
                datetime_element.get_attribute("datetime"))

            if date < datetime.date.today():
                continue

            date_and_time = datetime_element.text
            time = date_and_time.split('@ ')[-1]
            link_element = events[i].find_element(
                By.CSS_SELECTOR, "a.tribe-events-calendar-list__event-title-link")
            title = link_element.text
            link = link_element.get_attribute("href")
            link_element.click()

            new_window = self.driver.window_handles[-1]
            self.driver.switch_to.window(new_window)

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

            event_dict = {
                "Title": title,
                "Date": date.strftime("%B %d, %Y"),
                "Time": time,
                "Link": link,
                "Description": description,
                "Posted": False,
                "Passed": False
            }
            self.events.append(event_dict)

        self.driver.quit()


if __name__ == "__main__":
    scra = SouthCarolinaResearchAuthority()
    scra.get_events()
