from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Driver:
    """Class the initiates the web driver used for scraping"""

    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

        
