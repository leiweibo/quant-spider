import time
from io import BytesIO
from PIL import Image
import base64
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

EMAIL = 'cqc@cuiqingcai.com'
PASSWORD = ''
BORDER = 6
INIT_LEFT = 60


class CrackGeetest():
    def __init__(self):
        self.url = 'https://xueqiu.com'
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(chrome_options = self.chrome_options)
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD
    
    '''
    浏览器打开网址，并且填入账号密码，然后点击登录按钮，出现图形验证码
    '''
    def prepare_for_login(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        
        login_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'Header_nav__login__btn_1YU')))
        login_btn.click()
        user_name = self.wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password = self.wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        user_name.send_keys('15669761293')
        password.send_keys('')
        real_login_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'Loginmodal_modal__login__btn_uk7')))
        real_login_btn.click()

    '''
    导出canvas到png图片中
    '''
    def save_captcha_img(self, img_name, class_name):
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        getImgJS = 'return document.getElementsByClassName("' + class_name + '")[0].toDataURL("image/png");'
        img = self.browser.execute_script(getImgJS)
        base64_data_img = img[img.find(',') + 1:]
        image_base = base64.b64decode(base64_data_img)
        file = open(img_name, 'wb')
        file.write(image_base)
        file.close()

    def crack(self):
        # 访问网站并且输入用户名和密码，然后点击验证码按钮
        self.prepare_for_login()
        # 保存图片t
        # image1 = self.get_geetest_image()
        self.save_captcha_img('captcha1.png', 'geetest_canvas_fullbg')
        self.save_captcha_img('captcha2.png','geetest_canvas_bg')

        time.sleep(10)
        self.browser.quit()
        # # 点按呼出缺口
        # slider = self.get_slider()
        # slider.click()
        # # 获取带缺口的验证码图片
        # image2 = self.get_geetest_image('captcha2.png')
        # # 获取缺口位置
        # gap = self.get_gap(image1, image2)
        # print('缺口位置', gap)
        # # 减去缺口位移
        # gap -= BORDER
        # # 获取移动轨迹
        # track = self.get_track(gap)
        # print('滑动轨迹', track)
        # # 拖动滑块
        # self.move_to_gap(slider, track)
        
        # success = self.wait.until(
        #     EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
        # print(success)
        
        # # 失败后重试
        # if not success:
        #     self.crack()
        # else:
        #     self.login()


if __name__ == '__main__':
    crack = CrackGeetest()
    crack.crack()