# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging

from .base import Page


class PageLogin(Page):

    LOGIN = "login"
    USERNAME = "username"
    PASSWORD = "password"
    REMEMBER_USER = "remember_user"

    def __init__(self, webdriver):
        super().__init__(webdriver)

        self.locators = Page.get_locators_by_cfg("conf/login_pmarks.json")
        logging.debug("Get locators in %s page :", self.__class__.__name__)
        logging.debug(self.locators)
