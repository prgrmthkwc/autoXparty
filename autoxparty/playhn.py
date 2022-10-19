import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder

from . import helpers

ELEMENT = 'element'
COURSE_TYPE = 'course_type'
COURSE_SCORE = 'course_score'
COURSE_PROGRESS = 'course_progress'

WAIT_LD_TIMEOUT = 10  # 10 sec
WAIT_LD_SHORT = 3  # 3 sec
WAIT_USER_INPUT_TIMEOUT = 180  # 3 min
WAIT_CLASS_OVER = 5 # the suggestion is 5s (同时只能打开一门课程,请关闭之前页面,并于5秒后重试！)

WAIT_PLAYING_TICK = 10

KEY_LINKTEXT = "lnktext"
KEY_TABXPATH = "tabxpath"
KEY_ULXPATH = "ulxpath"
IDX_SPEC = 0
IDX_LEARNING = 1
CDITEMS = [
    {
        KEY_LINKTEXT : "指定课程",
        KEY_TABXPATH : "//div[@class='tab-panel perlist' and @ng-show='vm.activeTab == 2']",
        KEY_ULXPATH : "//div[2]/ul"
    },
    {
        KEY_LINKTEXT : "在学课程",
        KEY_TABXPATH : "//div[@class='tab-panel perlist' and @ng-show='vm.activeTab == 1']",
        KEY_ULXPATH : "//div[2]/div/ul"
    },
]


class Play:
    def __init__(self, webdrv, test: unittest.TestCase, username) -> None:
        self.webdrv_main = webdrv
        self.winhandle_main = webdrv.current_window_handle

        self.test = test
        self.score = -1
        self.specified_socre_is_not_enough = True
        self.course_list = []

        self.username = username

    def make_sure_login(self):
        webdrv = self.webdrv_main

        WebDriverWait(webdrv, WAIT_USER_INPUT_TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tm-user-info-new"))
        )

        def userinfo_is_ready(driver):
            user_info_name_div = driver.find_element(By.XPATH,
                    "//div[contains(@class, 'user_info_name')]")
            return self.username in user_info_name_div.text

        WebDriverWait(webdrv, WAIT_USER_INPUT_TIMEOUT).until(userinfo_is_ready)


        # get user's score:
        ul = webdrv.find_element(By.CLASS_NAME, "info_list")
        score = -1
        for li in ul.find_elements(By.TAG_NAME, "li"):
            txt = li.text

            print("\nitem ==>")
            print(txt)

            if txt.startswith("获得总学时"):
                score = int(float(txt[txt.index('（')+1: txt.index('）')]))
                self.score = score
            elif txt.startswith("指定课程学时"):
                s = txt[txt.index('：')+1:]
                ss = [t.strip() for t in s.split('|')]
                print("must get score is :", ss[1])
                print("==>> currently what you got is :", ss[0])
                self.specified_socre_is_not_enough = float(ss[0]) < float(ss[1])

        if score > 52:
            print("Congraduation VVVVV : you passed!")
        elif score == -1:
            print("Errrrrrooorr, you need check HTML code, failed to get the score.")
            return False
        else:
            print("\n\n ==========>>>>>\n Currently you just win socre: " + str(score))
            print(" Keeeeeeeeeeeep going.")

        return True

    def make_sure_course_list_data_is_ready(self, d):
        time.sleep(WAIT_LD_SHORT)
        webdrv = self.webdrv_main
        my_center = webdrv.find_element(By.CLASS_NAME, "my_center_container")
        my_center.find_element(By.PARTIAL_LINK_TEXT, d.get(KEY_LINKTEXT)).click()
        time.sleep(WAIT_LD_SHORT)
        print("switch to 指定课程==>")

        WebDriverWait(webdrv, WAIT_LD_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, d.get(KEY_TABXPATH)))
        )

        ul = WebDriverWait(webdrv, WAIT_LD_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, d.get(KEY_ULXPATH))))

        # print("TEXT in ul is:", ul.text)
        try:
            for li in ul.find_elements(By.TAG_NAME, "li"):
                tmp = li.text # check if data is really ready
        except StaleElementReferenceException:
            ul = WebDriverWait(webdrv, WAIT_LD_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, d.get(KEY_ULXPATH))))
            for li in ul.find_elements(By.TAG_NAME, "li"):
                tmp = li.text
                # print(tmp)

        return ul

    def prepare_specify_courses(self):
        self.make_sure_start_from_mainpage()
        time.sleep(WAIT_LD_SHORT)
        if self.specified_socre_is_not_enough:
            ul = self.make_sure_course_list_data_is_ready(CDITEMS[IDX_SPEC])
            self.get_unscored_course_list(ul)

    def prepare_courses(self):
        self.make_sure_start_from_mainpage()
        time.sleep(WAIT_LD_SHORT)
        ul = self.make_sure_course_list_data_is_ready(CDITEMS[IDX_LEARNING])
        self.get_unscored_course_list(ul)

    def get_unscored_course_list(self, ul):

        for li in ul.find_elements(By.TAG_NAME, "li"):
            d = dict()
            d[ELEMENT] = li

            txt = li.text.replace('\n', ' ').split(' ')
            for t in txt:
                t = t.strip()
                if t.startswith('课程类型'):
                    d[COURSE_TYPE] = t[t.index('：')+1:]
                elif t.startswith('课程学时'):
                    d[COURSE_SCORE] = t[t.index('：')+1:]
                elif t.endswith('%'):
                    d[COURSE_PROGRESS] = float(t[: -1])
            if d[COURSE_PROGRESS] < 100:
                self.course_list.append(d)

        for d in self.course_list:
            print(d)

    def start_game(self):
        webdrv = self.webdrv_main

        if len(self.course_list) == 0:
            print("course_list is empty. get NOTHING to play. QUIT.")
            return

        for item in self.course_list:
            self.make_sure_start_from_mainpage()

            li = item.get(ELEMENT)
            ActionChains(webdrv).move_to_element(li).perform()  # scroll to the item
            time.sleep(1)

            while not li.is_displayed():
                print("waiting li is ready after scrolling...")
                time.sleep(1)

            li.find_element(By.PARTIAL_LINK_TEXT, '开始学习').click()
            webdrv.switch_to.window(webdrv.window_handles[1])
            WebDriverWait(webdrv, WAIT_LD_TIMEOUT).until(EC.presence_of_element_located((By.XPATH,
                    "//span[@class='glyphicon glyphicon-play-circle']"))
            )
            webdrv.find_element(By.PARTIAL_LINK_TEXT, '点击播放').click()
            webdrv.switch_to.window(webdrv.window_handles[2])

            self.drag_and_drop_slider_to_startgame()
            if item.get(COURSE_TYPE) == '三分屏':
                self.get_iframes_to_play()
            elif item.get(COURSE_TYPE) == '单视频':
                self.just_play_a_video()

    def make_sure_playbar_displayed(self):
        webdrv = self.webdrv_main

        # view = webdrv.get_window_size()
        # w = view['width']
        # h = view['height']
        ### we need viewport size :
        w = int(webdrv.execute_script("return document.documentElement.clientWidth"))
        h = int(webdrv.execute_script("return document.documentElement.clientHeight"))
        qw = int(w/4)
        qh = int(h/4)

        for dw in range(-qh, qh, 10): # delta w for step
            for dh in range(5, qh, 5): # delta h for step
                vx = w/2+dw
                vy = h-dh
                action = ActionBuilder(webdrv)
                action.pointer_action.move_to_location(vx, vy)
                action.perform()
                print("mouse move_to_location(%d, %d)......" % (vx, vy))
                btn = self.get_playbar_element()
                if btn is not None:
                    print("mouse move_to_location(%d, %d) worked!" % (vx, vy))
                    return btn

        print("failed to get playbar elements !!!!!!!!!!!!!!")
        return None

    def get_playbar_element(self):
        webdrv = self.webdrv_main

        try:
            btn = WebDriverWait(webdrv, 1).until(
                EC.visibility_of_element_located((By.ID, "myplayer_display_button_play")))
        except TimeoutException as ex:
            print("failed to get it by ID: myplayer_display_button_play'")
        else:
            return btn

        try:
            btn = WebDriverWait(webdrv, 1).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".jwplay button")))
        except TimeoutException as ex:
            print("failed to get it by CSS_SELECTOR: .jwplay button'")
        else:
            return btn

        # try:
        #     btn = WebDriverWait(webdrv, WAIT_LD_SHORT).until(lambda d:
        #         d.find_element(By.ID, "myplayer_controlbar_duration"))
        # except TimeoutException as ex:
        #     print("failed to get it by CSS_SELECTOR: .jwplay button'")
        # else:
        #     return btn

        return None

    def just_play_a_video(self):
        webdrv = self.webdrv_main

        controlbar = WebDriverWait(webdrv, WAIT_LD_TIMEOUT).until(lambda d:
                d.find_element(By.ID, "myplayer_controlbar"))

        time.sleep(WAIT_LD_TIMEOUT)

        btn = self.make_sure_playbar_displayed()
        ActionChains(webdrv).move_to_element(btn).perform()

        def elapsed_time_is_ready(driver):
            elapsed = driver.find_element(By.ID, "myplayer_controlbar_elapsed")
            if ':' not in elapsed.text:
                print("faild to get elapse time:", elapsed.text)
                return False

            elapsed_time = helpers.time2secs(elapsed.text)
            return elapsed_time > 0

        WebDriverWait(webdrv, WAIT_LD_TIMEOUT).until(elapsed_time_is_ready)

        duration = controlbar.find_element(By.ID, "myplayer_controlbar_duration")
        dur_time_secs = helpers.time2secs(duration.text)

        elapsed_time = 0
        while elapsed_time/dur_time_secs < 0.82:

            self.close_msgbox_if_pop()

            # ActionChains(webdrv).move_to_element(btn).perform()
            elapsed = controlbar.find_element(By.ID, "myplayer_controlbar_elapsed")
            etime_text = webdrv.execute_script("return arguments[0].textContent", elapsed)
            if ':' not in etime_text:
                print("etime_text :", etime_text)
                continue
            elapsed_time = helpers.time2secs(etime_text)

            progress = int(elapsed_time/dur_time_secs * 10)
            print("progress: [%s]" % (progress*'#' + (10-progress)*'.'))

            time.sleep(WAIT_PLAYING_TICK)

    def get_iframes_to_play(self):
        webdrv = self.webdrv_main

        WebDriverWait(webdrv, WAIT_USER_INPUT_TIMEOUT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//iframe[@frameborder='0']"))
        )
        webdrv.switch_to.frame(0)

        WebDriverWait(webdrv, WAIT_USER_INPUT_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "iframe"))
        )
        webdrv.switch_to.frame("iframe")  # get to the nested iframe

        WebDriverWait(webdrv, WAIT_LD_TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "study-btn"))
        )
        webdrv.find_element(By.CLASS_NAME, 'continue-study').click()

        WebDriverWait(webdrv, WAIT_LD_TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "control-section"))
        )
        playbtn_div = webdrv.find_element(By.CLASS_NAME, "control-section")

        dur_time_secs = -1
        while dur_time_secs <= 0:
            duration = playbtn_div.find_element(
                By.XPATH, ".//span[@id='duration']").text
            print("duration:", duration)
            dur_time_secs = helpers.time2secs(duration)
            print("the course's total time is :", dur_time_secs)

            time.sleep(WAIT_LD_SHORT)

        cur_time_secs = 0
        while cur_time_secs/dur_time_secs < 0.82:

            self.close_msgbox_if_pop()

            self.answer_questions_if_pop()

            if len(playbtn_div.find_elements(By.XPATH, ".//span[@id='current_time']")) > 0:
                playing = playbtn_div.find_element(
                    By.XPATH, ".//span[@id='current_time']")
                if playing.is_displayed():
                    current = playing.text
                    cur_time_secs = helpers.time2secs(current)

            print("=====> the current playing time is :", cur_time_secs)
            time.sleep(WAIT_PLAYING_TICK)

        # when game done. need to switch back to default page.
        webdrv.switch_to.default_content()

    def close_msgbox_if_pop(self):
        webdrv = self.webdrv_main

        def close_msgbox(msgbox):
            if msgbox.is_displayed():  # shown on the screen
                btn = msgbox.find_element(By.TAG_NAME, "button")
                print("To dismiss message box ==>>", btn.text)
                btn.click()

        ## for 三分屏
        is_msgbox_present = len(webdrv.find_elements(By.CLASS_NAME, "message-box")) > 0
        if is_msgbox_present:
            msgbox = webdrv.find_element(By.CLASS_NAME, "message-box")
            close_msgbox(msgbox)

        ## for 单视频
        msgboxes = webdrv.find_elements(By.CLASS_NAME, "jy-msgbox")
        if msgboxes:
            close_msgbox(msgboxes[0])
            


    def answer_questions_if_pop(self):
        webdrv = self.webdrv_main
        is_ques_present = len(webdrv.find_elements(
            By.ID, "test_container")) > 0
        if is_ques_present:
            ques_ul = webdrv.find_element(By.ID, "test_container")
            if ques_ul.is_displayed():  # shown on the screen
                print("questions shown....")
                li = ques_ul.find_element(By.CLASS_NAME, "dis_block")
                test_title = li.find_element(By.XPATH, ".//h4//span[@class='test-title']").text.strip()
                print("to answer :", test_title)
                if test_title == "【多选题】":
                    self.answer_checkbox_questions(li)
                elif test_title == "【单选题】":
                    self.answer_radio_questions(li)

    def answer_radio_questions(self, li):
        # WebDriverWait(self.webdrv_main, WAIT_LD_TIMEOUT).until(
        #     EC.presence_of_element_located((By.XPATH, ".//span[@class='error']"))
        # )
        # tips = li.find_element(By.XPATH, ".//span[@class='error']").text.strip()
        # important!!! a work around to the span:
        # <li> ... <span class="error">回答不正确，正确答案:B</span> </li>
        #####
        tips = self.webdrv_main.execute_script("return arguments[0].innerHTML;",
                li.find_element(By.XPATH, './/span[@class="error"]'))
        t = tips.strip()
        key = t[t.rfind(':')+1:]  # "B" etc.

        print("get answer: %s and submit it" % key)

        li.find_element(By.XPATH, ".//*//input[@type='radio' and @value='%s']" % key[0]).click()
        li.find_element(By.XPATH, ".//*//input[@type='button' and @value='提交']").click()

    def answer_checkbox_questions(self, li):
        print("li.text = ", li.text)
        # tips = li.find_element(By.XPATH, ".//span[contains(@class,'error')]")
        # tips = li.find_element(By.CLASS_NAME, "error")
        # important!!! a work around to the span:
        # <li> ... <span class="error">回答不正确，正确答案:ABCD</span> </li>
        #####
        tips = self.webdrv_main.execute_script("return arguments[0].innerHTML;",
                li.find_element(By.XPATH, './/span[@class="error"]'))
        t = tips.strip()
        # print("error tips in span is : ", t)

        keys = t[t.rfind(':')+1:]  # "ABCD" etc.
        print("keys:", keys)

        for k in keys:
            print("check ...", k)
            li.find_element(By.XPATH, ".//*//input[@type='checkbox' and @value='%s']" % k).click()

        print("get answer: %s and submit it" % keys)
        li.find_element(By.XPATH, ".//*//input[@type='button' and @value='提交']").click()

    def drag_and_drop_slider_to_startgame(self):
        webdrv = self.webdrv_main

        WebDriverWait(webdrv, WAIT_LD_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "drag")))
        drag_div = webdrv.find_element(By.ID, "drag")

        slider = drag_div.find_element(By.CSS_SELECTOR, ".handler")

        action = ActionChains(webdrv)
        action.drag_and_drop_by_offset(slider, 300, 0).perform()

    def make_sure_start_from_mainpage(self):
        webdrv = self.webdrv_main

        # make sure it starts from main page ("personal center/ course list")
        if len(webdrv.window_handles) > 1:
            for h in webdrv.window_handles:
                if h != self.winhandle_main:  # make sure other tabs closed
                    webdrv.switch_to.window(h)
                    webdrv.close()
                    time.sleep(WAIT_CLASS_OVER)

            webdrv.switch_to.window(self.winhandle_main)
