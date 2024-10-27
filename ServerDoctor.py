import re
from time import sleep
from WebDriver import WebDriver as wd
from UI import UI

class ServerDoctor:
    def __init__(self, serverLink: str, driver: wd = wd()):
        self.serverLink = serverLink 
        self.driver = driver

    def getServerResponse(self) -> str:
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

        return match.group(1) if match else None 

    def isServerRunning(self) -> bool:
        serverResponse = self.getServerResponse()

        closedRoomMessages = ["The room was closed.", "Master connection error", "Connection closed"]
        if not serverResponse or serverResponse.startswith(tuple(closedRoomMessages)):
            return False
        
        return True