import re
from time import sleep
from WebDriver import WebDriver as wd
from Logs import Logs as Logger
from server_enums.OutputType import OutputType

class ServerDoctor:
    def __init__(self, serverLink: str, logger=Logger):
        self.serverLink = serverLink
        self.logger = logger 
        self.driver = wd(logger=self.logger)

    def getServerResponse(self) -> str:
        try:
            self.driver.getPage(self.serverLink)

            iFrame = self.driver.findElementByCSS(path='iframe[src*="game.html"]')
            self.driver.switchToFrame(iFrame)

            input_box = self.driver.findElementByCSS(path='input[data-hook="input"]')
            input_box.send_keys("@here")

            button = self.driver.findElementByCSS(path='button[data-hook="ok"]')
            button.click()

            sleep(10)
            page_source = self.driver.wd.page_source
            match = re.search(r'<p data-hook="reason">(.*?)<\/p>', page_source)

            self.driver.wd.close()
            self.driver.wd.quit()
            self.driver = wd(logger=self.logger)

            if match:
                return match.group(1) 
            if not match:
                self.logger.addLog(f"The doctor couldn't find the response :c", OutputType.ERROR, True)
        
        except Exception as error:
            self.logger.addLog(f"The doctor is sick :c we can't trust him {str(error)}", OutputType.ERROR, True)
            return ""

    def isServerRunning(self) -> bool:
        serverResponse = self.getServerResponse()

        closedRoomMessages = ["The room was closed.", "Master connection error", "Connection closed"]
        if serverResponse.startswith(tuple(closedRoomMessages)):
            return False

        return True