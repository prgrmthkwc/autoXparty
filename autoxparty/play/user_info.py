# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging

from .base import Play
from autoxparty.page.user_info import PageUserInfo


class UserInfo(Play):
    def __init__(self, webdrive, username=""):
        super(UserInfo, self).__init__(webdrive)
        self.page = PageUserInfo(webdrive, username)

    def start(self):
        logging.info("..............")
        self.page.make_sure_login()
        logging.info("......login!")
        self.page.make_sure_user_info_loaded()
        logging.info("......user info loaded!")
        self.page.load_scores()

        return True

    def reload_scores(self):
        self.webdriver.refresh()
        self.page.make_sure_user_info_loaded()
        self.page.load_scores()

    def is_class_over(self):
        return self.page.is_class_over()

    def is_spec_score_enough(self):
        return self.page.is_spec_score_enough()
