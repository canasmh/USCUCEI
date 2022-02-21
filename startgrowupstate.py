from driver import Driver
from selenium.webdriver.common.by import By
import time


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
        print(n_events)

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
            )

            date = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div[1]/div'
            )

            description = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[7]/div[2]/div/div/div/div/div[1]'
            )

            start_time = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div'
            )

            link_button = self.driver.find_element(
                By.XPATH,
                '//*[@id="hyperbaseContainer"]/div[15]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[5]/div[2]/div/div/div/a'
            )

            link = link_button.get_attribute("href")

            print("n: " + str(n) + "\n" + title.text + "\n" + date.text + "\n" + start_time.text + "\n" + end_time.text + "\n" + link + "\n" + description.text + "\n")
            time.sleep(0.5)
            n += 1

        self.driver.quit()
