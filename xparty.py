import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from autoxparty import helpers
from autoxparty.playhn import Play


class XpartyOnline(unittest.TestCase):

    def setUp(self) -> None:

        d = helpers.get_configs('xparty.cfg.json')
        self.username = d['username']
        self.url = d['url']

        chrome_opts = Options()
        chrome_opts.add_argument("--user-data-dir=" + self.username + "-data-dir")
        chrome_opts.add_argument("--mute-audio")
        # chrome_opts.add_argument("--headless")
        # chrome_opts.add_argument("--disable-gpu")
        # chrome_opts.add_argument("--window-size=1920,1200")
        # chrome_opts.add_argument("--disable-extensions")
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
        play = Play(webdrv, self, self.username)
        self.assertTrue(play.make_sure_login())
        play.prepare_courses()
        play.start_game()


if __name__ == '__main__':
    unittest.main()
