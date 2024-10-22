import re
from time import sleep
from WebDriver import WebDriver as wd

class ServerDoctor:
    def __init__(self, serverLink: str, wDriver: wd = wd([], "/usr/bin/chromedriver")):
        self.serverLink = serverLink 
        self.wDriver = wDriver

    def getServerResponse(self) -> str:
        self.wDriver.getPage(self.serverLink)

        iFrame = self.wDriver.findElementByCSS(path='iframe[src*="game.html"]')
        self.wDriver.switchToFrame(iFrame)

        input_box = self.wDriver.findElementByCSS(path='input[data-hook="input"]')
        input_box.send_keys("@here")

        button = self.wDriver.findElementByCSS(path='button[data-hook="ok"]')
        button.click()

        sleep(10)
        page_source = self.wDriver.wd.page_source
        match = re.search(r'<p data-hook="reason">(.*?)<\/p>', page_source)

        return match.group(1) if match else None 

    def isServerRunning(self) -> bool:
        serverResponse = self.getServerResponse()

        closedRoomMessages = ["The room was closed.", "Master connection error", "Connection closed"]
        if not serverResponse or serverResponse.startswith(tuple(closedRoomMessages)):
            return False
        
        print(serverResponse)
        return True

# sd = ServerDoctor("https://www.haxball.com/play?c=xswPO5QtLjw")
# sd.checkServerStatus()