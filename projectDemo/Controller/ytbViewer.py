from Controller.chromController import ChromeController
from selenium.webdriver.common.by import By

class ytbViewer(ChromeController):
    def __init__(self) -> None:
        super().__init__()

    def OpenYtb(self, search_query):
        self.open_chrome()

        self.do_sendkey(element=(By.XPATH, "//input[@name='search_query']"), time_wait=35, text=search_query)

        self.do_click(element=(By.XPATH, "//button[@id='search-icon-legacy']"), time_wait=35, double_click=False)

        self.do_click(element=(By.XPATH, "(//ytd-video-renderer[@class='style-scope ytd-item-section-renderer'])[1]//a[@id='thumbnail']"), time_wait=30, double_click=True)
