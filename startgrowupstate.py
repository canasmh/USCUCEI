import datetime

from driver import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import date


def format_date(event_date):

    month, day, year = event_date.split("/")
    event_date = datetime.date(int(year), int(month), int(day))

    return event_date


class StartGrowUpstate(Driver):

    def __init__(self):
        super().__init__()
        self.url = "https://www.startgrowupstate.com/explore-events"
        self.events = []

    def get_events(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        calendar_object = self.driver.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(calendar_object)
        n = 0
        events = self.driver.find_elements(By.CSS_SELECTOR, ".calendarRecord")
        n_events = len(events)

        events[n].click()
        while n < n_events:
            next_event_button = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[1]/div/div/div/div[1]/div[3]'
             )
            next_event_button.click()

            title = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/div/div'
            ).text

            event_date = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div[1]/div'
            ).text

            event_date = format_date(event_date)

            if event_date < date.today():
                n += 1
                continue

            description = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[7]/div[2]/div/div/div/div/div[1]'
            ).text

            start_time = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div'
            ).text

            try:
                end_time = self.driver.find_element(
                    By.XPATH,
                    '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div'
                ).text
            except NoSuchElementException:
                end_time = "Not Specified"

            link_button = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[5]/div[2]/div/div/div/a'
            )

            link = link_button.get_attribute("href")

            event_dict = {
                "Title": title,
                "Date": event_date.strftime("%B %d, %Y"),
                "Time": start_time + " - " + end_time,
                "Link": link,
                "Description": description
            }

            self.events.append(event_dict)
            n += 1

        self.driver.quit()

if __name__ == "__main__":
    sgu = StartGrowUpstate()
    sgu.get_events()