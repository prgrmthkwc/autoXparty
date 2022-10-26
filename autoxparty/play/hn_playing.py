# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging
import time

from .login import Login
from .user_info import UserInfo
from .course_list import CourseList
from .course_detail import CourseDetail
from .drag_slider import DragSlider
from .playing_1vmode import PlayingMode1v
from .playing_3bmode import PlayingMode3b


class HnPlaying:
    TIMEOUT_CLASS_OVER: int = 5  # 5secs
    WAITING_BEFORE_APP_QUIT: int = 60  # 1 minute

    def __init__(self, webdriver, username, password):
        self.webdriver = webdriver
        self.username = username
        self.password = password
        self.mainwin_handle = webdriver.current_window_handle

    def make_sure_on_main_window(self):
        wb = self.webdriver
        if wb.current_window_handle == self.mainwin_handle:
            return
        for handle in reversed(wb.window_handles):
            if handle != self.mainwin_handle:
                wb.switch_to.window(handle)
                wb.close()
                time.sleep(HnPlaying.TIMEOUT_CLASS_OVER)
        wb.switch_to.window(self.mainwin_handle)

    def start(self):
        wb = self.webdriver
        login_page = Login(wb, self.username, self.password)
        login_page.start()

        user_info_page = UserInfo(wb, self.username)
        user_info_page.start()

        while not user_info_page.is_class_over():

            to_learn_spec_course = not user_info_page.is_spec_score_enough()
            course_list = CourseList(wb, to_learn_spec_course)
            if not course_list.start():
                logging.info("Nothing to learn. The application will quit after %d seconds.",
                             HnPlaying.WAITING_BEFORE_APP_QUIT)
                time.sleep(HnPlaying.WAITING_BEFORE_APP_QUIT)
                return

            wb.switch_to.window(wb.window_handles[1])
            course_detail = CourseDetail(wb)
            course_detail.start()
            wb.switch_to.window(wb.window_handles[2])

            drag = DragSlider(wb)
            drag.start()

            if course_list.course_type_is_mode_1v():
                play1v = PlayingMode1v(wb)
                play1v.start()
            elif course_list.course_type_is_mode_3b():
                play3b = PlayingMode3b(wb)
                play3b.start()
                wb.switch_to.default_content()
            else:
                logging.error("Get unknown course type: %s", course_list.get_current_course_type())

            self.make_sure_on_main_window()
            user_info_page.reload_scores()
