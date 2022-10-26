# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging

from .base import Page
from selenium.webdriver.common.by import By


class PageUserInfo(Page):
    DIV_USER_INFO = "div_user_info"
    DIV_USER_INFO_NAME = "div_user_info_name"
    UL_INFO_LIST = "ul_info_list"

    TARGET_SCORE = 52.0

    def __init__(self, webdriver, username):
        super().__init__(webdriver)

        self.score = -1.0
        self.target_score = PageUserInfo.TARGET_SCORE
        self.spec_score = -1.0
        self.target_spec_score = -1.0

        self.username = username
        self.locators = Page.get_locators_by_cfg("conf/user_info_pmarks.json")

        logging.debug("Get locators in %s page :", self.__class__.__name__)
        logging.debug(self.locators)

    def make_sure_login(self):
        self.make_sure_visibility_of_element_after_user_input(
            self.locators.get(PageUserInfo.DIV_USER_INFO))

    def make_sure_user_info_loaded(self):
        def user_info_loaded(driver):
            hello = self.get_displayed_element(self.locators.get(PageUserInfo.DIV_USER_INFO_NAME))
            logging.info("hello msg: %s", hello.text)
            return self.username in hello.text

        self.wait.until(user_info_loaded)

    def load_scores(self):
        ul = self.get_displayed_element(self.locators.get(PageUserInfo.UL_INFO_LIST))
        for li in ul.find_elements(By.TAG_NAME, "li"):
            s = li.text
            if s.startswith("获得总学时"):
                self.score = float(s[s.index('（') + 1: s.index('）')])
            elif s.startswith("指定课程学时"):
                x = s[s.index('：') + 1:]
                ss = [t.strip() for t in x.split('|')]
                self.target_spec_score = float(ss[1])
                self.spec_score = float(ss[0])

        logging.info("需要完成指定学时: %.1f", self.target_spec_score)
        logging.info("当前完成指定: %.1f", self.spec_score)
        logging.info("需要完成总学时: %.1f", self.target_score)
        logging.info("当前已获得总学时: %.1f", self.score)

    def is_class_over(self):
        if self.score < 0:
            return False
        return self.spec_score >= self.target_spec_score and self.score >= self.target_score

    def is_spec_score_enough(self):
        return self.spec_score >= self.target_spec_score
