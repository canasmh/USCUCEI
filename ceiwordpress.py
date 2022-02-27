from driver import Driver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

load_dotenv()


class CEIWordPress(Driver):

    def __init__(self):
        super().__init__()
        self.url = os.environ.get("WP_URL")

    def post_events(self):
        self.driver.get(self.url)


if __name__ == "__main__":
    wp = CEIWordPress()
    wp.post_events()
