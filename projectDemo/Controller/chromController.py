from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

class ChromeController:
    def __init__(self) -> None:
        self.driver = None
    
    def open_chrome(self, url=None):
        chrome_options = Options()
        service = Service(ChromeDriverManager().install()) 

        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("--mute-audio")  
        chrome_options.add_argument("--window-size=800,600")
        chrome_options.add_experimental_option("detach", True)
        
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get(url or "https://www.youtube.com/")
    
    def do_click(self, element, time_wait, double_click=False):
        try:
            WebDriverWait(self.driver, time_wait).until(
                EC.element_to_be_clickable(element)
            )
            elem = self.driver.find_element(*element)
            
            if double_click:
                print("Click đôi")
                actions = ActionChains(self.driver)
                actions.double_click(elem).perform()
            else:
                elem.click()
                print("Click đơn")
        except Exception as e:
            print(f"Đã xảy ra lỗi khi thực hiện click: {e}")

    def do_sendkey(self, element, time_wait, text):
        try:
            WebDriverWait(self.driver, timeout=time_wait).until(
                EC.presence_of_element_located(element)
            ).send_keys(text)
        except Exception as e:
            print(f"Đã xảy ra lỗi khi gửi key: {e}")

    def do_scroll(self, direction="down", amount=500):
        try:
            if direction == "down":
                self.driver.execute_script(f"window.scrollBy(0, {amount});")
            elif direction == "up":
                self.driver.execute_script(f"window.scrollBy(0, -{amount});")
        except Exception as e:
            print(f"Đã xảy ra lỗi khi cuộn trang: {e}")

