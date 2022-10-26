# -*- coding: utf-8 -*-
# (C) 2022 编程不想｜prgrmthkwc

import logging

from .base import Page


class PagePlayingMode1v(Page):

    VIDEO_AREA = "video_area"

    CTRLBAR = "ctrlbar"
    CTRLBAR_PLAY_BTN_ID = "ctrlbar_play_btn_id"
    CTRLBAR_PLAY_BTN_CSS = "ctrlbar_play_btn_css"

    SPAN_DURATION = "span_duration"
    SPAN_ELAPSED = "span_elapsed"

    MSGBOX = "msgbox"
    MSGBOX_OK_BTN = "msgbox_ok_btn"

    def __init__(self, webdriver):
        super().__init__(webdriver)

        self.locators = Page.get_locators_by_cfg("conf/playing_1vmode_pgmarks.json")
        logging.debug("Get locators in %s page :", self.__class__.__name__)
        logging.debug(self.locators)
