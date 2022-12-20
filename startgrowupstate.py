from driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import date
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

    event_date = date(int(event_date[-4:]), convert_month[event_date[0:3]], int(event_date[4:6]))

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
            time.sleep(0.01)

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

            new_event = {
                'Title': '',
                'Date': '',
                'Time': 'N/A',
                'Link': '',
                'Description': '',
            }

            """
            COMMENT: This page is very verrryyy interesting. Theres a total of like 10 classes used through out the whole thing
            and there aren't very many unique edintifiers for the elements I need access to...

            So I'm getting the calendar_container using XPATH, and then getting calendar items, children of calendar_container.

            The problem is, that the XPath to the container... changes ? 🤔 so thats what the following try block checks..
            
            """
            try:
                calendar_container = self.driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div[3]")
                calendar_item = calendar_container.find_elements(By.CLASS_NAME, f"GroupItem")[i - 1]
            except (IndexError, NoSuchElementException) as e:
                print(e)
                calendar_container = self.driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[3]")
                calendar_item = calendar_container.find_elements(By.CLASS_NAME, f"GroupItem")[i - 1]
            link_to_event_page = calendar_item.find_element(By.TAG_NAME, "a")
            link = link_to_event_page.get_attribute("href")
            self.driver.get(link)
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(2)

            title = self.driver.find_element(By.TAG_NAME, "h3")

            new_event['Title'] = title.text.strip()

            try: 
                text_container = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]")
            except NoSuchElementException:
                text_container = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]")
            
            text_elements = text_container.find_elements(By.CLASS_NAME, "Text")
            

            key = None
            for t_element in text_elements:

                if t_element.text.strip().lower() == "about this event":
                    key = 'Description'
                    continue

                elif t_element.text.strip().lower() == "date":    
                    key ='Date'
                    continue
                
                if key is None:
                    print("no key... ")
                    continue
                    
                elif key == "Date":
                    event_date = t_element.text.split(" - ")[0].strip()
                    new_event[key] += format_date(event_date)
                    
                else:
                    new_event[key] += t_element.text.strip()
            

            link_to_event_info = self.driver.find_element(By.LINK_TEXT, "Visit Website for More")
            new_event['Link'] = link_to_event_info.get_attribute("href")
            self.events.append(new_event)
            print(new_event)
            print("")

            back_button = self.driver.find_element(By.LINK_TEXT, "Back to the Events Directory")
            back_button.click()
            self.driver.switch_to.window(self.driver.window_handles[0])
            i += 1

        self.driver.quit()


if __name__ == "__main__":
    sgu = StartGrowUpstate()
    sgu.get_events()
    edb = EventsDB(sgu.events, 'test')
    edb.add_events()
