# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging

from .base import Page


class PageCourseDetail(Page):

    PLAY_ICON = "play_icon"
    PLAY_LINK_TEXT = "play_link_text"

    def __init__(self, webdriver):
        super().__init__(webdriver)

        self.locators = Page.get_locators_by_cfg("conf/course_detail_pmarks.json")
        logging.debug("Get locators in %s page :", self.__class__.__name__)
        logging.debug(self.locators)
