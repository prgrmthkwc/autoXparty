# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from autoxparty import helpers

from .playing import Playing
from autoxparty.page.playing_1vmode import PagePlayingMode1v as Ppm1v


class PlayingMode1v(Playing):

    PAUSE_VIDEO_TRICK = 10  # 10 secs

    def __init__(self, webdriver):
        super(PlayingMode1v, self).__init__(webdriver)
        self.page = Ppm1v(webdriver)
        self.action = ActionBuilder(webdriver)
        self.mouse_offset_w = 0
        self.mouse_offset_h = 0
        self.video_area = None

    def make_sure_video_time_shown(self):
        self._move_mouse_to(self.mouse_offset_w, self.mouse_offset_h)

        def elapsed_time_is_ready(driver):
            loc = self.page.get_locator(Ppm1v.SPAN_ELAPSED)
            elapsed = driver.find_element(*loc)
            if ':' not in elapsed.text:
                logging.warning("Failed to get elapse time: %s", elapsed.text)
                return False

            elapsed_time = helpers.time2secs(elapsed.text)
            return elapsed_time > 0

        self.page.wait.until(elapsed_time_is_ready)
        loc = self.page.get_locator(Ppm1v.VIDEO_AREA)
        self.video_area = self.webdriver.find_element(*loc)

    def get_time_in_span(self, mark):
        loc = self.page.get_locator(mark)
        t = self.page.get_displayed_element(loc, self.playbar)
        return helpers.time2secs(t.text)

    def update_video_time_values(self):
        self.make_sure_video_time_shown()
        self.elapsed_secs = self.get_time_in_span(Ppm1v.SPAN_ELAPSED)
        self.duration_secs = self.get_time_in_span(Ppm1v.SPAN_DURATION)
        self.is_short_video = self.duration_secs <= Playing.SHORT_VIDEO

    def prepare_playing(self):
        # set elapsed_secs/duration_secs/is_short_video
        loc = self.page.get_locator(Ppm1v.CTRLBAR)
        self.playbar = self.page.wait.until(lambda d: d.find_element(*loc))
        self.moving_mouse_to_get_playbar_displayed()
        self.update_video_time_values()

    def get_play_btn(self):
        try:
            btn = self.page.wait_tick.until(EC.visibility_of_element_located(
                self.page.get_locator(Ppm1v.CTRLBAR_PLAY_BTN_ID)))
        except TimeoutException as ex:
            logging.info("failed to get it by ID: myplayer_display_button_play'")
        else:
            return btn

        try:
            btn = self.page.wait_tick.until(EC.visibility_of_element_located(
                self.page.get_locator(Ppm1v.CTRLBAR_PLAY_BTN_CSS)))
        except TimeoutException as ex:
            logging.info("failed to get it by CSS_SELECTOR: .jwplay button'")
        else:
            return btn

    def _move_mouse_to(self, w, h):
        self.action.pointer_action.move_to_location(w, h)
        self.action.perform()

    def moving_mouse_to_get_playbar_displayed(self):
        webdrv = self.webdriver
        # view = webdrv.get_window_size()
        # w = view['width']
        # h = view['height']
        ### we need viewport size :
        w = int(webdrv.execute_script("return document.documentElement.clientWidth"))
        h = int(webdrv.execute_script("return document.documentElement.clientHeight"))
        qw = int(w / 4)
        qh = int(h / 4)

        for dw in range(-qh, qh, 10):  # delta w for step
            for dh in range(5, qh, 5):  # delta h for step
                vx = w / 2 + dw
                vy = h - dh
                self._move_mouse_to(vx, vy)
                logging.info("mouse move_to_location(%d, %d)......", vx, vy)
                btn = self.get_play_btn()
                if btn is not None:
                    logging.info("mouse move_to_location(%d, %d) worked!", vx, vy)
                    self.mouse_offset_w = vx
                    self.mouse_offset_h = vy
                    ActionChains(self.webdriver).move_to_element(btn).perform()
                    return
        logging.error("failed to get playbar elements !!!!!!!!!!!!!!")

    def answer_question_if_popup(self):
        pass

    def dismiss_msgbox_if_popup(self):
        loc = self.page.get_locator(Ppm1v.MSGBOX)
        mbs = self.webdriver.find_elements(*loc)
        if mbs:
            Playing.dismiss_msgbox(mbs[0])

    def class_is_over(self):
        if self.duration_secs <= 0:
            logging.warning("duration in seconds is : .1f%", self.duration_secs)
            return False
        percent = Playing.PERCENT4NORMAL
        if self.is_short_video:
            percent = Playing.PERCENT4SHORT
        return self.elapsed_secs / self.duration_secs >= percent

    def running(self):
        self.update_video_time_values()
        tick = Playing.TICKTOK
        if self.is_short_video:
            tick = Playing.TICK
            if self.elapsed_secs / self.duration_secs > Playing.PERCENT4NORMAL:
                # make it pause for a moment
                logging.warning("!!!!! click the video to make it paused")
                ActionChains(self.webdriver).click(self.video_area).perform()
                time.sleep(PlayingMode1v.PAUSE_VIDEO_TRICK)
                logging.warning("The trick DONE. Now resume it to playing")
                ActionChains(self.webdriver).click(self.video_area).perform()

        time.sleep(tick)
