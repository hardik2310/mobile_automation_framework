import time

import pytest
from appium.webdriver.appium_service import AppiumService

from utilities import read_utils

"""It is not working."""


@pytest.fixture(scope = "session", autouse = True)
def start_appium_server():
    config_data = read_utils.get_dictionary_from_json("../test_data/config.json")
    service = AppiumService()
    service.start(args = ['-p', config_data['port'], '-a', 'localhost', '--relaxed-security', '--base-path', '/wd/hub'])
    print(service.is_running)
    print(service.is_listening)
    # os.system("start /B start cmd.exe @cmd /k appium")
    # os.system("start /B start cmd.exe @cmd /k appium -a 127.0.0.1 -p 4728")
    yield
    time.sleep(5)
    service.stop()
    # os.system("taskkill /F /IM node.exe")
    # os.system("taskkill /F /IM cmd.exe")
