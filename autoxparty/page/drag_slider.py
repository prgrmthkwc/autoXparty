import logging

from selenium.webdriver.common.action_chains import ActionChains

from .base import Page


class PageDragSlider(Page):

    DIV_DRAG = "div_drag"
    DIV_SLIDER = "div_slider"

    DRAG_OFFSET = 300

    def __init__(self, webdriver):
        super().__init__(webdriver)

        self.locators = Page.get_locators_by_cfg("conf/drag_slider_pmarks.json")
        logging.debug("Get locators in %s page :", self.__class__.__name__)
        logging.debug(self.locators)

    def drag_slider(self):
        drag_div = self.make_sure_visibility_of_element_located(self.get_locator(PageDragSlider.DIV_DRAG))
        slider = self.get_located_element(self.get_locator(PageDragSlider.DIV_SLIDER), drag_div)
        action = ActionChains(self.webdriver)
        action.drag_and_drop_by_offset(slider, PageDragSlider.DRAG_OFFSET, 0).perform()
