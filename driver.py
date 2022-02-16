from selenium import webdriver
import os


class Driver:

    def __init__(self):
        self.driver_path = os.getcwd() + "/chromedriver"
        self.driver = webdriver.Chrome(self.driver_path)

        