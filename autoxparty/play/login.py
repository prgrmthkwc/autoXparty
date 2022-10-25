from .base import Play
from autoxparty.page.login import PageLogin


class Login(Play):
    def __init__(self, webdriver, username="", password=""):
        super(Login, self).__init__(webdriver)
        self.page = PageLogin(webdriver)
        self.username = username
        self.password = password

    def input_txt(self, by_mark, txt):
        loc = self.page.get_locator(by_mark)
        editor = self.page.get_displayed_element(loc)
        editor.clear()
        editor.send_keys(txt)

    def start(self):
        loc_login = self.page.get_locator(PageLogin.LOGIN)
        self.page.make_sure_visibility_of_element_located(loc_login)

        if len(self.username) > 0:
            self.input_txt(PageLogin.USERNAME, self.username)
        if len(self.password) > 0:
            self.input_txt(PageLogin.PASSWORD, self.password)

        return True
