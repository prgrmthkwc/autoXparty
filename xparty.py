#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from autoxparty import helpers
from autoxparty.playhn import Play

CFG_USERNAME = 'username'
CFG_PASSWORD = "password"
CFG_GATE_URL = "url"
CFG_TARGET_SCORE = "score"

DEFAULT_TARGET_SCORE = 52

VERSION_AUTOXPARTY = "1.0"
RELEASE_DATE = "2022/10/19"
COPYRIGHT_INFO = "Copyright(c) prgrmthkwc(PTWC) & 编程不想"


class XpartyOnline(unittest.TestCase):

    def setUp(self) -> None:

        print("\n\n")
        print("autoXparty version:", VERSION_AUTOXPARTY)
        print("release date:", RELEASE_DATE)
        print("Copyright info:\n", COPYRIGHT_INFO)
        print("\n\n")

        d = helpers.get_configs('xparty.cfg.json')
        self.assertTrue(CFG_USERNAME in d, msg="You MUST specify the 'username' value in 'xparty.cfg.json' file!")
        self.username = d[CFG_USERNAME]
        self.assertTrue(CFG_GATE_URL in d, msg="You MUST specify the 'url' value in 'xparty.cfg.json' file!")
        self.url = d[CFG_GATE_URL]

        self.target_score = DEFAULT_TARGET_SCORE
        if CFG_TARGET_SCORE in d:
            self.target_score = d[CFG_TARGET_SCORE]
        self.password = ""
        if CFG_PASSWORD in d:
            self.password = d[CFG_PASSWORD]

        chrome_opts = Options()
        if platform.system() != 'Windows':
            chrome_opts.add_argument("--user-data-dir=" + self.username + "-data-dir")
        chrome_opts.add_argument("--mute-audio")
        chrome_opts.add_argument("--disable-gpu")
        chrome_opts.add_argument("--disable-extensions")
        # chrome_opts.add_argument("--headless")
        # chrome_opts.add_argument("--window-size=1920,1200")
        # chrome_opts.add_argument("--no-sandbox")
        # chrome_opts.add_argument("--remote-debugging-port=9222")

        self.webdrv = webdriver.Chrome(options=chrome_opts,
                service=ChromeService(ChromeDriverManager().install()))

        return super().setUp()

    def tearDown(self) -> None:
        self.webdrv.quit()
        return super().tearDown()

    def test_startXparty(self):
        webdrv = self.webdrv
        webdrv.get(self.url)
        play = Play(webdrv, self,
                self.username, self.password, self.target_score)
        play.login_game()
        self.assertTrue(play.make_sure_login())

        play.prepare_specify_courses()
        play.start_game()

        play.prepare_courses()
        play.start_game()


if __name__ == '__main__':
    unittest.main()
