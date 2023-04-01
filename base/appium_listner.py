import time

import pytest
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from utilities import read_utils


class AppiumConfig:
    driver = None
    json_dic = None
    wait = None

    @pytest.fixture(scope = "function", autouse = True)
    def handle_app_launch(self):
        self.json_dic = read_utils.get_dictionary_from_json("../test_data/config.json")
        des_cap = {"platformName": self.json_dic["platformName"], "deviceName": self.json_dic["deviceName"]}
        self.driver = webdriver.Remote(command_executor = self.json_dic['server'] + self.json_dic['port'] + "/wd/hub", desired_capabilities = des_cap)
        self.driver.implicitly_wait(30)
        self.wait = WebDriverWait(self.driver, 10)

        yield
        time.sleep(3)
        self.driver.quit()
