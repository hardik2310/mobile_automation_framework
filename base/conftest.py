import time

# import pytest
from appium.webdriver.appium_service import AppiumService

from utilities import read_utils

"""It is not working."""

# @pytest.fixture(scope="session", autouse=True)
def start_appium_server():
    config_data = read_utils.get_dictionary_from_json("../test_data/config.json")
    service = AppiumService()
    service.start(args=['-p', config_data['port'], '-a', 'localhost', '--relaxed-security', '--base-path', '/wd/hub'])
    print(service.is_running)
    print(service.is_listening)
    yield
    time.sleep(5)
    service.stop()
