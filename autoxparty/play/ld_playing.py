# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging
from operator import le
import time

from selenium.common.exceptions import TimeoutException

from .login import Login
from .playing_3bmode import PlayingMode3b
from .user_info import UserInfo
from .ld_course_list import LdCourseList
from .course_detail import CourseDetail
from .drag_slider import DragSlider
from .playing_1vmode import PlayingMode1v


class LdPlaying:
    WAITING_SWITCH_TAB: int = 3
    TIMEOUT_CLASS_OVER: int = 5  # 5secs
    WAITING_BEFORE_APP_QUIT: int = 60  # 1 minute
    WAITING_TRAINING_COURSE_LOADING = 10  # 10 secs

    def __init__(self, webdriver, username, password, training_url):
        self.webdriver = webdriver
        self.username = username
        self.password = password
        self.mainwin_handle = webdriver.current_window_handle
        self.training_url = training_url
        assert training_url is not None

    def make_sure_on_main_window(self):
        wb = self.webdriver
        if wb.current_window_handle == self.mainwin_handle:
            return
        for handle in reversed(wb.window_handles):
            if handle != self.mainwin_handle:
                wb.switch_to.window(handle)
                wb.close()
                time.sleep(LdPlaying.TIMEOUT_CLASS_OVER)
        wb.switch_to.window(self.mainwin_handle)
        time.sleep(LdPlaying.TIMEOUT_CLASS_OVER)

    def start(self):
        wb = self.webdriver
        login_page = Login(wb, self.username, self.password)
        login_page.start()

        user_info_page = UserInfo(wb, self.username)
        user_info_page.start()

        wb.get(self.training_url)
        time.sleep(LdPlaying.WAITING_TRAINING_COURSE_LOADING)

        spec = LdCourseList(wb)
        course_list = spec.get_course_list()
        if course_list is None:
            logging.error("failed to get the course list.")

        # list[0] is the title bar, skip it
        for item in course_list[1:]:

            logging.info("item text: %s", item.text)

            if spec.check_if_course_need_to_learn(item):
                spec.set_current_course(item)
                spec.start()

                wb.switch_to.window(wb.window_handles[1])
                time.sleep(LdPlaying.WAITING_SWITCH_TAB)
                course_detail = CourseDetail(wb)
                course_detail.start()

                wb.switch_to.window(wb.window_handles[2])
                time.sleep(LdPlaying.WAITING_SWITCH_TAB)
                drag = DragSlider(wb)
                drag.start()

                play3b = PlayingMode3b(wb)
                if play3b.is_3bmode():
                    play3b.start()
                else:
                    play1v = PlayingMode1v(wb)
                    play1v.start()

                self.make_sure_on_main_window()

    def check_course_type_is_3bmode(self):
        play3b = PlayingMode3b(self.webdriver)
        return play3b.is_3bmode()
