# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from .base import Page


class PageLdCourseList(Page):
    MUST_LEARN = "must_learn"
    TAB_CONTAINER = "tab_container"

    TAB_SPEC_COURSE = "tab_spec_course"
    COURSE_LIST = "course_list"

    PROGRESS = "progress"
    CLICK = "click"

    def __init__(self, webdriver):
        super().__init__(webdriver)

        self.locators = Page.get_locators_by_cfg("conf/ld_course_list_pmarks.json")
        logging.info("Get locators in %s page :", self.__class__.__name__)
        logging.info(self.locators)

    def load_learning_course_list(self):
        logging.info("load_learning_course_list ...")
        # spec_course_link = self.get_displayed_element(self.get_locator(PageLdCourseList.MUST_LEARN))
        # spec_course_link.click()

        tab_container = self.get_locator(PageLdCourseList.TAB_CONTAINER)
        tab_content = self.make_sure_presence_of_element_located(tab_container)

        tab_spec = self.get_locator(PageLdCourseList.TAB_SPEC_COURSE)
        tab = self.make_sure_presence_of_element_located(tab_spec)

        loc = self.get_locator(PageLdCourseList.COURSE_LIST)
        return tab.find_elements(*loc)

    def check_if_course_need_to_learn(self, item):
        loc = self.get_locator(PageLdCourseList.PROGRESS)
        logging.info("progress mark is : %s", PageLdCourseList.PROGRESS)
        logging.info(loc)
        p = item.find_element(*loc).text.strip()
        progress = float(p[:"".rfind('%')])
        logging.info("the progress is %s ==> %.1f", p, progress)
        return progress < 100

    def learn_course(self, item):
        loc = self.get_locator(PageLdCourseList.CLICK)
        link = item.find_element(*loc)

        ActionChains(self.webdriver).move_to_element(link).perform()
        self.make_sure_element_is_visible(link)

        link.click()
