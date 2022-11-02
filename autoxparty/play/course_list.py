# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging

from .base import Play
from autoxparty.page.course_list import PageCourseList
from autoxparty.page.base import Page


class CourseList(Play):

    def __init__(self, webdriver=None, learn_spec_course=False):
        super(CourseList, self).__init__(webdriver)
        self.webdriver = webdriver
        self.to_learn_spec_course = learn_spec_course
        self.page = PageCourseList(webdriver)
        self.course = None

    def start(self):
        # get course ready
        ul = None
        if self.to_learn_spec_course:
            ul = self.page.load_spec_course_list()
        else:
            ul = self.page.load_learning_course_list()

        if not ul:
            logging.warning("Failed to get course list. Had you done your work?")
            return False

        self.course = self.page.get_course_to_learn(ul)
        if self.course:
            self.page.learn_course()
            return True

        if self.to_learn_spec_course:  # get to the next page if it has
            if self.get_to_next_page():
                return self.start()

        return False

    def get_to_next_page(self):
        return self.page.get_to_next_page()

    def get_current_course_type(self):
        return self.course.get(PageCourseList.TYPE)

    def course_type_is_mode_3b(self):
        return self.course.get(PageCourseList.TYPE) == Page.COURSE_TYPE_3BLOCK

    def course_type_is_mode_1v(self):
        return self.course.get(PageCourseList.TYPE) == Page.COURSE_TYPE_1VIDEO
