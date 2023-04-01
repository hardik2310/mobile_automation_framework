from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.extensions.android.nativekey import AndroidKey
from assertpy import assert_that
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from base.appium_listner import AppiumConfig


class TestAndroidDeviceLocal(AppiumConfig):
    def test_click_photos(self):
        self.driver.activate_app(self.json_dic["cameraApp"])
        self.wait = WebDriverWait(self.driver, 10)
        self.wait.until(ec.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Shutter")))
        for i in range(4):
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Shutter").click()
            self.wait.until(ec.presence_of_element_located((AppiumBy.ID, "com.android.camera2:id/rounded_thumbnail_view")))

        self.driver.find_element(AppiumBy.ID, "com.android.camera2:id/rounded_thumbnail_view").click()
        size_dic = self.driver.get_window_size()
        x1 = size_dic['width'] * (75 / 100)
        y1 = size_dic['height'] * (50 / 100)

        x2 = size_dic['width'] * (25 / 100)
        y2 = size_dic['height'] * (50 / 100)
        for _ in range(3):
            self.driver.swipe(x1, y1, x2, y2, 1000)
        self.driver.find_element(AppiumBy.XPATH, "//android.widget.ImageView[2]").click()
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Delete").click()

        actual_text = self.driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[1]").text
        assert_that(actual_text).is_equal_to("Deleted")

        self.driver.press_keycode(AndroidKey.BACK)
        self.wait.until(ec.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Shutter")))
        self.driver.terminate_app(self.json_dic["cameraApp"])

    def test_on_off_bluetooth(self):
        self.wait = WebDriverWait(self.driver, 10)
        size_dic = self.driver.get_window_size()
        x1 = size_dic['width'] * (50 / 100)
        y1 = size_dic['height'] * (1 / 100)
        x2 = size_dic['width'] * (50 / 100)
        y2 = size_dic['height'] * (75 / 100)
        self.driver.swipe(x1, y1, x2, y2, 1000)

        bluetooth_value = self.driver.find_element(AppiumBy.XPATH, "//android.widget.Switch[@content-desc='Bluetooth.']").get_attribute('checked')
        action = TouchAction(self.driver)
        if bluetooth_value == 'false':
            action.tap(self.driver.find_element(AppiumBy.XPATH, "//android.widget.Switch[@content-desc='Bluetooth.']")).perform()
        bluetooth_value = self.driver.find_element(AppiumBy.XPATH, "//android.widget.Switch[@content-desc='Bluetooth.']").get_attribute('checked')
        assert_that(bluetooth_value).is_equal_to('true')

        size_dic = self.driver.get_window_size()
        x1 = size_dic['width'] * (50 / 100)
        y1 = size_dic['height'] * (75 / 100)
        x2 = size_dic['width'] * (50 / 100)
        y2 = size_dic['height'] * (5 / 100)
        self.driver.swipe(x1, y1, x2, y2, 1000)
        self.wait.until(ec.presence_of_element_located((AppiumBy.XPATH, "//android.widget.TextView[@content-desc='Messages']")))

        self.driver.activate_app(self.json_dic["settingApp"])
        self.wait.until(ec.presence_of_element_located((AppiumBy.XPATH, "//*[@text='Settings']")))

        self.driver.find_element(AppiumBy.XPATH, "//*[@text='Search settings']").click()
        self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").clear()
        self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").send_keys("Blue")

        self.wait.until(ec.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@text,'Connected devices >')]")))
        bluetooth_value = self.driver.find_element(AppiumBy.XPATH, "//android.widget.LinearLayout[1]/android.widget.Switch").get_attribute('checked')
        assert_that(bluetooth_value).is_equal_to('true')

        self.driver.find_element(AppiumBy.XPATH, "//android.widget.LinearLayout[1]/android.widget.Switch").click()
        bluetooth_value = self.driver.find_element(AppiumBy.XPATH, "//android.widget.LinearLayout[1]/android.widget.Switch").get_attribute('checked')
        assert_that(bluetooth_value).is_equal_to('false')

        size_dic = self.driver.get_window_size()
        x1 = size_dic['width'] * (50 / 100)
        y1 = size_dic['height'] * (1 / 100)

        x2 = size_dic['width'] * (50 / 100)
        y2 = size_dic['height'] * (75 / 100)

        self.driver.swipe(x1, y1, x2, y2, 1000)
        bluetooth_value = self.driver.find_element(AppiumBy.XPATH, "//android.widget.Switch[@content-desc='Bluetooth.']").get_attribute('checked')
        assert_that(bluetooth_value).is_equal_to('false')
        self.driver.press_keycode(AndroidKey.HOME)

    def test_setting_accessibility(self):
        self.driver.activate_app(self.json_dic["settingApp"])
        para_dic = {"strategy": AppiumBy.ANDROID_UIAUTOMATOR, "selector": 'UiSelector().text("Accessibility")'}
        self.driver.execute_script("mobile: scroll", para_dic)

        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'UiSelector().text("Accessibility")').click()
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'UiSelector().text("Timing controls")').click()

        self.driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Time to take action')]").click()
        self.driver.find_element(AppiumBy.XPATH, "//android.widget.LinearLayout[3]/android.widget.LinearLayout[1]/android.widget.RadioButton").click()
        checked_value = self.driver.find_element(AppiumBy.XPATH, "//android.widget.LinearLayout[3]/android.widget.LinearLayout[1]/android.widget.RadioButton").get_attribute('checked')
        assert_that(checked_value).is_equal_to('true')
        self.driver.terminate_app(self.json_dic["settingApp"])
