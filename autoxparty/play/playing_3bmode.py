# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from autoxparty import helpers

from .playing import Playing
from autoxparty.page.playing_3bmode import PagePlayingMode3b as Ppm3b


class PlayingMode3b(Playing):
    MODE1_QUESTION = 1
    MODE2_JUST_WATCHING = 2

    def __init__(self, webdriver):
        super(PlayingMode3b, self).__init__(webdriver)
        self.page = Ppm3b(webdriver)
        self.mode = PlayingMode3b.MODE1_QUESTION

    def check_if_just_watching_mode(self):
        time.sleep(self.page.TIMEOUT_LOAD_LIST)
        try:
            loc = self.page.get_locator(Ppm3b.DIV_CONTINUE_STUDY)
            box = self.page.wait.until(EC.visibility_of_element_located(loc))
            return box
        except TimeoutException:
            logging.info("It's not the Just Play Video mode.")
            return None

    def continue_to_play_mode1(self):
        loc = self.page.get_locator(Ppm3b.BTN_CONTINUE_STUDY)
        study = self.page.wait.until(EC.presence_of_element_located(loc))
        study.click()

    def switch_iframe_to_play(self):
        loc = self.page.get_locator(Ppm3b.IFRAME_1)
        self.page.wait.until(EC.presence_of_element_located(loc))
        self.webdriver.switch_to.frame(0)
        logging.info("switch to frame 1")

        box = self.check_if_just_watching_mode()

        if box:
            self.mode = PlayingMode3b.MODE2_JUST_WATCHING
            self.click_element(Ppm3b.DIV_USER_CHOICE)

        if self.mode == PlayingMode3b.MODE1_QUESTION:
            loc = self.page.get_locator(Ppm3b.IFRAME_2)
            self.page.wait.until(EC.presence_of_element_located(loc))
            self.webdriver.switch_to.frame(Ppm3b.IFRAME_PLAY)
            logging.info("switch to frame 2")

            self.continue_to_play_mode1()

    def make_sure_video_time_shown(self):

        loc = self.page.get_locator(Ppm3b.CTRL_SECTION)
        self.playbar = self.page.wait.until(EC.visibility_of_element_located(loc))

        def duration_time_is_ready(driver):
            duration = self.extract_element_text(Ppm3b.SPAN_DURATION, driver)
            if duration is None:
                return False
            duration_secs = helpers.time2secs(duration)
            return duration_secs > 0

        self.page.wait.until(duration_time_is_ready)

    def _get_time_in_span(self, mark):
        loc = self.page.get_locator(mark)
        t = self.page.get_displayed_element(loc, self.playbar)
        return helpers.time2secs(t.text)

    def update_video_time_values(self):
        self.elapsed_secs = self._get_time_in_span(Ppm3b.SPAN_ELAPSED)
        self.duration_secs = self._get_time_in_span(Ppm3b.SPAN_DURATION)

    def prepare_playing(self):
        self.switch_iframe_to_play()
        if self.mode == PlayingMode3b.MODE1_QUESTION:
            self.make_sure_video_time_shown()
            self.update_video_time_values()
        else:
            logging.warning("NOT implemented YEEEEEEEEEET!")

    def answer_question_if_popup(self):
        loc = self.page.get_locator(Ppm3b.TEST_CONTAINER)
        ul = self.page.wait.until(EC.presence_of_element_located(loc))
        if ul.is_displayed():
            loc = self.page.get_locator(Ppm3b.TEST_DIS_BLOCK)
            li = self.page.wait.until(EC.visibility_of_element_located(loc))
            tt = self.extract_element_text(Ppm3b.TEST_TITLE, li)
            logging.info("---------->> to answer question: %s", tt)
            if tt == Ppm3b.MULTI_CHOICES_TITLE:
                self.answer_checkbox_question(li)
            elif tt == Ppm3b.SINGLE_CHOICE_TITLE:
                self.answer_radio_question(li)

    def get_answer_tips(self, li):
        loc = self.page.get_locator(Ppm3b.QUESTION_ANSWER_TIPS)
        span_error = li.find_element(*loc)

        tips = self.webdriver.execute_script("return arguments[0].innerHTML;", span_error)
        return tips.strip()

    def answer_checkbox_question(self, li):
        t = self.get_answer_tips(li)
        keys = t[t.rfind(':') + 1:]  # "ABCD" etc.

        for k in keys:
            loc = self.page.get_locator(Ppm3b.ANSWER_CHECKBOX_BUILDER)
            li.find_element(loc[0], loc[1] % k).click()

        logging.info("=========>> submit the answer: %s", keys)
        self.click_element(Ppm3b.ANSWER_SUBMIT_BTN, li)

    def answer_radio_question(self, li):
        t = self.get_answer_tips(li)
        key = t[t.rfind(':') + 1:]  # "B" etc.

        logging.info("=========>> get answer: %s and submit it", key[0])

        loc = self.page.get_locator(Ppm3b.ANSWER_RADIO_BUILDER)
        li.find_element(loc[0], loc[1] % key[0]).click()

        self.click_element(Ppm3b.ANSWER_SUBMIT_BTN, li)

    def dismiss_msgbox_if_popup(self):
        loc = self.page.get_locator(Ppm3b.MSGBOX)
        mbs = self.webdriver.find_elements(*loc)
        if mbs:
            Playing.dismiss_msgbox(mbs[0])

    def class_is_over(self):
        if self.duration_secs <= 0:
            logging.warning("duration in seconds is : .1f%", self.duration_secs)
            return False
        return self.elapsed_secs / self.duration_secs >= Playing.PERCENT4NORMAL

    def running(self):
        self.update_video_time_values()
        time.sleep(Playing.TICKTOK)

    def is_3bmode(self):
        webdriver = self.webdriver
        time.sleep(10)
        loc = self.page.get_locator(Ppm3b.IFRAME_1)
        try:
            self.page.wait.until(EC.presence_of_element_located(loc))
        except TimeoutException:
            return False
        else:
            self.webdriver.switch_to.frame(0)

            try:
                loc = self.page.get_locator(Ppm3b.IFRAME_2)
                self.page.wait.until(EC.presence_of_element_located(loc))
                return True
            except TimeoutException:
                return False
            finally:
                webdriver.switch_to.default_content()
