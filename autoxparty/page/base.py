import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from autoxparty import helpers


class Page:
    TIMEOUT_LOADING_ELEMENT = 10  # 10 sec
    TIMEOUT_WAITING_USER_INPUT = 1800  # 30min
    TIMEOUT_LOAD_LIST = 3  # 3 secs
    TIMEOUT_SCROLL_VIEW = 2  # 2 secs
    TIMEOUT_TICK = 1  # 1 sec

    COURSE_TYPE_3BLOCK = "三分屏"
    COURSE_TYPE_1VIDEO = "单视频"

    BY_MAPS = {
        "ID": By.ID,
        "XPATH": By.XPATH,
        "LINK_TEXT": By.LINK_TEXT,
        "PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT,
        "NAME": By.NAME,
        "TAG_NAME": By.TAG_NAME,
        "CLASS_NAME": By.CLASS_NAME,
        "CSS_SELECTOR": By.CSS_SELECTOR
    }

    @staticmethod
    def get_locators_by_cfg(page_marks_conf: str):
        cfg = helpers.get_configs(page_marks_conf)

        d = dict()
        for key, vd in cfg.items():
            for k, v in vd.items():
                d[key] = (Page.BY_MAPS.get(k), v)

        return d

    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.locators = dict()
        self.wait = WebDriverWait(webdriver, Page.TIMEOUT_LOADING_ELEMENT)
        self.wait_tick = WebDriverWait(webdriver, Page.TIMEOUT_TICK)
        self.wait_user_input = WebDriverWait(webdriver, Page.TIMEOUT_WAITING_USER_INPUT)

    def _make_sure_presence_of_element_located(self, wait, locator):
        try:
            element = wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            logging.error("need check why not find the element: (%s, %s)" % locator)

    def make_sure_presence_of_element_located(self, locator):
        return self._make_sure_presence_of_element_located(self.wait, locator)

    def make_sure_presence_of_element_after_user_input(self, locator):
        return self._make_sure_presence_of_element_located(self.wait_user_input, locator)

    def _make_sure_visibility_of_element_located(self, wait, locator):
        try:
            element = wait.until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            logging.error("need check why the element is not displayed: (%s, %s)" % locator)

    def make_sure_visibility_of_element_located(self, locator):
        self._make_sure_visibility_of_element_located(self.wait, locator)

    def make_sure_visibility_of_element_after_user_input(self, locator):
        self._make_sure_visibility_of_element_located(self.wait_user_input, locator)

    def is_element_located(self, locator, parent=None):
        if parent is None:
            parent = self.webdriver
        elements = parent.find_elements(*locator)
        getit = len(elements) > 0

        return getit, elements[0] if getit else None

    def get_located_element(self, locator, parent=None):
        getit, element = self.is_element_located(locator, parent)
        if not getit:
            logging.error("Failed to get the located element:(%s, %s)", locator)
        return element

    def is_element_displayed(self, locator, parent=None):
        if parent is None:
            parent = self.webdriver
        elements = parent.find_elements(*locator)
        getit = len(elements) > 0
        if getit:
            getit = elements[0].is_displayed()

        return getit, elements[0] if getit else None

    def get_displayed_element(self, locator, parent=None):
        getit, element = self.is_element_displayed(locator, parent)
        if not getit:
            logging.error("Failed to get the displayed element:(%s, %s)", locator)
        return element

    def get_locator(self, by_mark: str):
        if by_mark in self.locators:
            return self.locators.get(by_mark)
        logging.error("failed to get the locator by :", by_mark)

    def make_sure_element_is_visible(self, element):
        try:
            return self.wait.until(EC.visibility_of(element))
        except TimeoutException:
            logging.error("need check why the element is not displayed")
