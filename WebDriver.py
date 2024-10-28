from typing import List
from server_enums.OutputType import OutputType as outType

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
import os

DEFAULT_ARGUMENTS = ["--no-sandbox",
                     "--disable-dev-shm-usage",
                     "--headless",
                     "--log-level=3",
                     "--silent",
                     "--disable-logging",
                     '--disable-setuid-sandbox',
                     '--disable-features=WebRtcHideLocalIpsWithMdns',
                     '--disable-component-extensions-with-background-pages',
                     '--disable-extensions',
                     '--disable-background-networking',
                     '--disable-hang-monitor',
                     '--mute-audio',
                     '--no-first-run',
                     '--disable-background-networking',
                     '--disable-breakpad',
                     '--disable-component-update',
                     '--disable-domain-reliability',
                     '--disable-sync',
                     '--metrics-recording-only',
                     '--no-zygote',
                     '--in-process-gpu']

DEFAULT_PATH = "/usr/bin/chromedriver"

class WebDriver:
    def __init__(self, arguments: List[str] = DEFAULT_ARGUMENTS, executablePath: str = DEFAULT_PATH, logger: Logs = None):
        options = ChromeOptions()
        for arg in arguments:
            options.add_argument(arg)
        
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
        options.add_experimental_option("detach", True)
        
        if "linux" in platform and executablePath:
            service = ChromeService(executable_path=executablePath, log_output=os.devnull)
        else:
            service = ChromeService(log_output=os.devnull)

        self.wd = webdriver.Chrome(service=service, 
                                   options=options,
                                   keep_alive=True)

        self.logger = logger

    def getPage(self, page: str):
        self.wd.get(page)

    def runScript(self, script: str):
        self.wd.execute_script(script)
        
    def getConsoleLogs(self, printLogs: bool):
        logs = self.wd.get_log("browser")
        if printLogs and self.logger:
            for entry in logs:
                log = f"{entry['level']}: {entry['message']}"
                self.logger.addLog(log, outType=outType.SERVER)
        return logs 

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

    