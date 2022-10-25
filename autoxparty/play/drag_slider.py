from .base import Play
from autoxparty.page.drag_slider import PageDragSlider


class DragSlider(Play):
    def __init__(self, webdriver):
        super(DragSlider, self).__init__(webdriver)
        self.page = PageDragSlider(webdriver)

    def start(self):
        self.page.drag_slider()
