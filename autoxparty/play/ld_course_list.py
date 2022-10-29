# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging

from .base import Play
from autoxparty.page.ld_course_list import PageLdCourseList
from autoxparty.page.base import Page


class LdCourseList(Play):

    def __init__(self, webdriver=None):
        super(LdCourseList, self).__init__(webdriver)
        self.webdriver = webdriver
        self.course = None

        self.page = PageLdCourseList(webdriver)

    def get_course_list(self):
        return self.page.load_learning_course_list()

    def check_if_course_need_to_learn(self, item):
        return self.page.check_if_course_need_to_learn(item)

    def set_current_course(self, item):
        self.course = item

    def start(self):
        
        if self.course is not None:
            self.page.learn_course(self.course)
            return True
        logging.error("get None course.")
        return False
