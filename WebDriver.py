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
from selenium.webdriver.remote.command import Command

from selenium.webdriver.firefox.service import Service as FirefoxOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager as GeckoManager

from webdriver_manager.chrome import ChromeDriverManager

import logging
from sys import platform
import os

DEFAULT_ARGUMENTS = ["--no-sandbox",
                     "--disable-dev-shm-usage",
                    #  "--headless",
                    #  "--log-level=3",
                    #  "--silent",
                    #  "--disable-logging",
                    #  "--enable-unsafe-swiftshader",
                    #  '--disable-setuid-sandbox',
                    #  '--disable-features=WebRtcHideLocalIpsWithMdns',
                    #  '--disable-component-extensions-with-background-pages',
                    #  '--disable-extensions',
                    #  '--disable-background-networking',
                    #  '--disable-hang-monitor',
                     '--mute-audio',
                    #  '--no-first-run',
                    #  '--disable-background-networking',
                    #  '--disable-breakpad',
                    #  '--disable-component-update',
                    #  '--disable-domain-reliability',
                    #  '--disable-sync',
                    #  '--metrics-recording-only',
                    #  '--no-zygote',
                    #  '--in-process-gpu',
                    #  '--allow-insecure-localhost', # may be a security risk idk :3
                    #  '--disable-low-res-tiling',
                     '--disable-gpu',
                     '--no-crash-upload',
                     '--disable-crash-reporter',
                    #  '--disable-client-side-phishing-detection',
                    #  '--disable-backgrounding-occluded-windows',
                    #  '--disable-background-timer-throttling',
                    #  '--disable-renderer-backgrounding',
                    #  '--disable-oopr-debug-crash-dump'
                    ]

DEFAULT_PATH = "/usr/bin/chromedriver"

class WebDriver:
    # def __init__(self, arguments: List[str] = DEFAULT_ARGUMENTS, executablePath: str = DEFAULT_PATH, logger: Logs = None):
    #     options = ChromeOptions()
    #     for arg in arguments:
    #         options.add_argument(arg)
        
    #     options.add_experimental_option("excludeSwitches", ["enable-logging"])
    #     options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    #     options.add_experimental_option("detach", True)

    #     driverLogPath = "logs/driverLogs.txt"

    #     driverLogger = logging.getLogger('selenium')
    #     driverLogger.setLevel(logging.DEBUG)
        
    #     handler = logging.FileHandler(driverLogPath)
    #     driverLogger.addHandler(handler)
        
    #     logging.getLogger('selenium.webdriver.remote').setLevel(logging.WARN)
    #     logging.getLogger('selenium.webdriver.common').setLevel(logging.DEBUG)
    #     logging.getLogger('selenium.webdriver.chrome').setLevel(logging.CRITICAL)

    #     if "linux" in platform:
    #         executablePath = ChromeDriverManager().install()
    #         service = webdriver.ChromeService(executable_path=executablePath, log_output=os.devnull)
    #     else:
    #         service = ChromeService(log_output=os.devnull)

    #     self.wd = webdriver.Chrome(service=service, 
    #                                options=options,
    #                                keep_alive=True)

    #     self.logger = logger


    def __init__(self, arguments: List[str] = DEFAULT_ARGUMENTS, executablePath: str = DEFAULT_PATH, logger: Logs = None):
        options = ChromeOptions()
        for arg in arguments:
            options.add_argument(arg)
        
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
        options.add_experimental_option("detach", True)

        driverLogPath = "logs/driverLogs.txt"

        driverLogger = logging.getLogger('selenium')
        driverLogger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler(driverLogPath)
        driverLogger.addHandler(handler)
        
        logging.getLogger('selenium.webdriver.remote').setLevel(logging.WARN)
        logging.getLogger('selenium.webdriver.common').setLevel(logging.DEBUG)
        logging.getLogger('selenium.webdriver.firefox').setLevel(logging.CRITICAL)

        if "linux" in platform:
            executablePath = GeckoManager().install()
            service = webdriver.FirefoxService(executable_path=executablePath, log_output=os.devnull)
        else:
            service = webdriver.FirefoxService(log_output=os.devnull)

        self.wd = webdriver.Firefox(service=service, 
                                           options=options,
                                           keep_alive=True)

        self.logger = logger

    def getPage(self, page: str):
        self.wd.get(page)

    def refreshPage(self):
        self.wd.refresh()

    def minimizeWindow(self):
        self.wd.minimize_window()

    def runScript(self, script: str):
        self.wd.execute_script(script)

    def getConsoleLogs(self, printLogs: bool) -> str:
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

    def isDriverAlive(self) -> bool:
        try:
            self.wd.execute(Command.REFRESH)
            return True
        except Exception as error:
            self.logger.addLog(f"Can't connect with driver:\n {error}", outType=outType.ERROR)
            return False