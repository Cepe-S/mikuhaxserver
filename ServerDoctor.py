from WebDriver import WebDriver as wd
from Logs import Logs as Logger
from server_enums.OutputType import OutputType

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import sys
import asyncio

class ServerDoctor:
    def __init__(self, serverLink: str, logger=Logger):
        self.serverLink = serverLink
        self.logger = logger 
        self.driver = wd(logger=self.logger)
        self.serverDied = asyncio.Event()

    async def getIntoPatient(self) -> str:
        try:
            self.driver.getPage(self.serverLink)

            iFrame = self.driver.findElementByCSS(path='iframe[src*="game.html"]')
            self.driver.switchToFrame(iFrame)

            input_box = self.driver.findElementByCSS(path='input[data-hook="input"]')
            input_box.send_keys("doctor")

            button = self.driver.findElementByCSS(path='button[data-hook="ok"]')
            button.click()

            self.driver.wd.switch_to.default_content()
            
            iFrame = self.driver.findElementByCSS(path='iframe[src*="game.html"]')
            self.driver.switchToFrame(iFrame)
            
            element = self.driver.findElementByCSS(path='input[data-hook="input"]')
            element.send_keys("!yoadmin");   element.send_keys(Keys.ENTER)
            element.send_keys("!powershot"); element.send_keys(Keys.ENTER)
            element.send_keys("!afk");       element.send_keys(Keys.ENTER)

            while True:
                try:
                    self.logger.addLog(message="Doctor is following the patient status", outType=OutputType.PROGRAM)
                    WebDriverWait(self.driver.wd, timeout=sys.float_info.max).until(EC.staleness_of(element))
                    self.logger.addLog(message="The server died （o´・ェ・｀o）", outType=OutputType.ERROR)
                    return True
                except TimeoutException:
                    self.logger.addLog(message="The doctor is tired and is going to take a 1 milisecond nap ✧₊・₍ᐢ˶-  ̫ -˶ᐢ₎ ᶻ 𝗓 𐰁・₊✧", 
                                       outType=OutputType.PROGRAM)
                    pass

        except Exception as error:
            self.logger.addLog(message=f"The doctor is sick :c we can't trust him {str(error)}", outType=OutputType.ERROR)
            return False