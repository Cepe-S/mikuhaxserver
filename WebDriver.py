from typing import List

from Logs import Logs

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from sys import platform
from datetime import datetime as dt

class WebDriver:
    def __init__(self, arguments: List[str], executablePath: str = ""):
        options = ChromeOptions()
        for arg in arguments:
            options.add_argument(arg)

        options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
        options.add_experimental_option("detach", True)
        
        service = ChromeService(executable_path=executablePath) if "linux" in platform and executablePath else None

        self.wd = webdriver.Chrome(service=service, 
                                   options=options)
    
        self.logger = Logs(dt.now())

    def getPage(self, page: str):
        self.wd.get(page)

    def runScript(self, script: str):
        self.wd.execute_script(script)

    def getConsoleLogs(self):
        logs = self.wd.get_log("browser")
        for entry in logs:
            log = f"{entry['level']}: {entry['message']}"
            print(log)
            self.logger.addLog(log)

    def findElementByCSS(self, path: str, time: int = 10) -> WebElement:    
        try:
            return WebDriverWait(self.wd, time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, path))
            )
        except NoSuchElementException:
            return None

    def findElementByXPath(self, path: str, time: int = 10) -> WebElement:
        try:
            return WebDriverWait(self.wd, time).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
        except NoSuchElementException:
            return None

    def switchToFrame(self, frame: WebElement):
        self.wd.switch_to.frame(frame)

    