import logging

from .base import Page


class PagePlayingMode3b(Page):
    IFRAME_1 = "iframe_container"
    IFRAME_2 = "iframe_play"
    IFRAME_PLAY = "iframe"

    # some page just has frame 1
    DIV_CONTINUE_STUDY = "div_continue_box"
    DIV_USER_CHOICE = "div_user_choice"

    BTN_START_STUDY = "btn_start_study"
    BTN_CONTINUE_STUDY = "btn_continue_study"

    CTRL_SECTION = "ctrl_section"
    SPAN_DURATION = "span_duration"
    SPAN_ELAPSED = "span_elapsed"

    MSGBOX = "msgbox"
    MSGBOX_OK_BTN = "msgbox_ok_btn"

    MULTI_CHOICES_TITLE = "【多选题】"
    SINGLE_CHOICE_TITLE = "【单选题】"

    TEST_CONTAINER = "test_container"
    TEST_DIS_BLOCK = "test_dis_block"
    TEST_TITLE = "test_title"
    QUESTION_ANSWER_TIPS = "question_answer_tips"
    ANSWER_RADIO_BUILDER = "answer_radio_builder"
    ANSWER_CHECKBOX_BUILDER = "answer_checkbox_builder"
    ANSWER_SUBMIT_BTN = "answer_submit_btn"

    def __init__(self, webdriver):
        super().__init__(webdriver)

        self.locators = Page.get_locators_by_cfg("conf/playing_3bmode_pgmarks.json")
        logging.debug("Get locators in %s page :", self.__class__.__name__)
        logging.debug(self.locators)
