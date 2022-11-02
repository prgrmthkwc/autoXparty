# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


from .base import Page


class PageCourseList(Page):

    MY_CENTER = "my_center_container"

    TAB_SPEC_LINK_TEXT = "tab_spec_link_text"
    TAB_SPEC_PANEL = "tab_spec_panel"
    TAB_SPEC_UL = "tab_spec_ul"

    TAB_LEARNING_LINK_TEXT = "tab_learning_link_text"
    TAB_LEARNING_PANEL = "tab_learning_panel"
    TAB_LEARNING_UL = "tab_learning_ul"

    LI_NEXT_PAGE = "li_next_page"

    LI_START_LINK_TEXT = "li_start_link_text"

    LI = 0
    TYPE = 1
    SCORE = 2
    PROGRESS = 3
    SIZE = 4

    def __init__(self, webdriver):
        super().__init__(webdriver)

        self.course = dict()

        self.locators = Page.get_locators_by_cfg("conf/course_list_pmarks.json")
        logging.debug("Get locators in %s page :", self.__class__.__name__)
        logging.debug(self.locators)

    def load_tab(self, marks):
        spec_course_link = self.get_displayed_element(self.get_locator(marks[0]))
        spec_course_link.click()
        self.make_sure_presence_of_element_located(self.get_locator(marks[1]))
        time.sleep(Page.TIMEOUT_LOAD_LIST)
        return self.make_sure_presence_of_element_located(self.get_locator(marks[2]))

    def load_spec_course_list(self):
        loc_my_center = self.get_locator(PageCourseList.MY_CENTER)
        self.make_sure_visibility_of_element_located(loc_my_center)
        return self.load_tab([PageCourseList.TAB_SPEC_LINK_TEXT,
                              PageCourseList.TAB_SPEC_PANEL,
                              PageCourseList.TAB_SPEC_UL])

    def load_learning_course_list(self):
        loc_my_center = self.get_locator(PageCourseList.MY_CENTER)
        self.make_sure_visibility_of_element_located(loc_my_center)
        return self.load_tab([PageCourseList.TAB_LEARNING_LINK_TEXT,
                              PageCourseList.TAB_LEARNING_PANEL,
                              PageCourseList.TAB_LEARNING_UL])

    def get_course_to_learn(self, ul):
        for li in ul.find_elements(By.TAG_NAME, "li"):
            txt = li.text.replace('\n', ' ').split(' ')
            logging.info("item in li: %s", txt)

            course_type = ""
            course_score = ""
            course_progress = 101
            for s in txt:
                t = s.strip()
                if t.startswith('课程类型'):
                    course_type = t[t.index('：') + 1:]
                elif t.startswith('课程学时'):
                    course_score = t[t.index('：') + 1:]
                elif t.endswith('%'):
                    course_progress = float(t[: -1])

            if course_progress < 100:
                self.course[PageCourseList.TYPE] = course_type
                self.course[PageCourseList.SCORE] = course_score
                self.course[PageCourseList.PROGRESS] = course_progress
                self.course[PageCourseList.LI] = li
                logging.info(" ==>> Get the course to learn:")
                logging.info("type:%s, score:%s, progress:%.1f%%",
                             course_type, course_score, course_progress)
                return self.course

        return None

    def learn_course(self):
        li = self.course.get(PageCourseList.LI)
        ActionChains(self.webdriver).move_to_element(li).perform()
        self.make_sure_element_is_visible(li)

        loc = self.get_locator(PageCourseList.LI_START_LINK_TEXT)
        li.find_element(*loc).click()

    def get_to_next_page(self):
        loc = self.get_locator(PageCourseList.LI_NEXT_PAGE)
        li = self.webdriver.find_element(*loc)
        if "disabled" == li.get_attribute("class"):
            return False
        li.click()
        logging.info("Get to the next page ...")
        time.sleep(Page.TIMEOUT_LOAD_LIST)
        return True
