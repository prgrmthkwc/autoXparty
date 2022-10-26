# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc



class Play:

    def __init__(self, webdriver=None):
        self.webdriver = webdriver
        self.page = None

    def start(self):
        return True

    def click_element(self, by_mark, parent=None):
        loc = self.page.get_locator(by_mark)
        p = parent if parent else self.webdriver
        p.find_element(*loc).click()

    def extract_element_text(self, by_mark, parent=None):
        loc = self.page.get_locator(by_mark)
        p = parent if parent else self.webdriver
        p.find_element(*loc).text.strip()
