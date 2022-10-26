# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

from selenium.webdriver.common.by import By

from .base import Play


class Playing(Play):
    TICK = 1  # 5 secs
    TICKTOK = 10  # 10 secs
    PERCENT4NORMAL = 0.82
    PERCENT4SHORT = 0.90
    SHORT_VIDEO = 180  # 3 minutes

    def __init__(self, webdriver):
        super(Playing, self).__init__(webdriver)
        self.playbar = None
        self.elapsed_secs = -1.0
        self.duration_secs = -1.0
        self.is_short_video = False

    @staticmethod
    def dismiss_msgbox(msgbox):
        if msgbox.is_displayed():  # shown on the screen
            ok = msgbox.find_element(By.TAG_NAME, "button")
            ok.click()

    def prepare_playing(self):
        # set elapsed_secs/duration_secs/is_short_video
        pass

    def answer_question_if_popup(self):
        pass

    def dismiss_msgbox_if_popup(self):
        pass

    def class_is_over(self):
        return True

    def running(self):
        pass

    def start(self):
        self.prepare_playing()
        while not self.class_is_over():
            self.dismiss_msgbox_if_popup()
            self.answer_question_if_popup()
            self.running()  # time.sleep() in it
