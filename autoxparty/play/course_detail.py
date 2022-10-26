# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging

from selenium.webdriver.support import expected_conditions as EC

from .base import Play
from autoxparty.page.course_detail import PageCourseDetail


class CourseDetail(Play):
    def __init__(self, webdriver):
        super(CourseDetail, self).__init__(webdriver)
        self.page = PageCourseDetail(webdriver)

    def start(self):
        loc = self.page.get_locator(PageCourseDetail.PLAY_ICON)
        logging.info("the locator is :(%s, %s)", *loc)
        self.page.wait.until(EC.presence_of_element_located(loc))
        self.click_element(PageCourseDetail.PLAY_LINK_TEXT)
